from src.Models.EventCamera import EventCamera
from sklearn.neighbors import kneighbors_graph, NearestNeighbors
from keras.utils import image_utils
from sklearn.metrics import silhouette_score
from sklearn.cluster import spectral_clustering
from sklearn.cluster import SpectralClustering
from sklearn.feature_extraction import image
import numpy
from scipy import ndimage
import matplotlib.pyplot as plt
import sys
import random
import pydantic
from src.Models.Visualizer import Visualizer
import typing
import matplotlib
from stonesoup.types.detection import Detection
from src.Enums.ModelModeEnum import ModelModeEnum


class GSCEventMOD(EventCamera):
    num_neighbors: int
    mode: ModelModeEnum

    # typing.Optional(X) encourages those variables to be X, otherwise they are type None
    # All threes values are set in config file
    # Minimum number of clusters
    min_num_clusters: typing.Optional[int] = None
    # Maximum number of clusters
    max_num_clusters: typing.Optional[int] = None
    # Actual number of clusters
    num_clusters: typing.Optional[int] = None

    #suggestion: maybe replace with math.inf, but depends on Python version
    #otherwise, try: (inf = float('inf')) except: inf = <high value, e.g. 1e3000> 
    max_score: float = float("infinity")
    optimal_clusters: int = 0 

    # Checks if max_num_clusters, min_num_clusters and num_clusters are set
    # Pydantic is library used for data validation/settings management
    @pydantic.root_validator()
    @classmethod
    def validate_mode(cls, field_values):
        print(field_values)
        mode: str = field_values["mode"]

        if mode == ModelModeEnum.FIND_OPTIMAL_CLUSTERS.value:
            if (
                "min_num_clusters" not in field_values
                or "max_num_clusters" not in field_values
            ):
                raise ValueError(
                    "Provide min_num_clusters and max_num_clusters to find the optimal number of clusters"
                )
        else:
            if "num_clusters" not in field_values:
                raise ValueError("Provide num_clusters in config in order to cluster")

        return field_values

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    # Not implemented yet
    def predict(self, input: numpy.array) -> None:
        raise NotImplemented("predict not implemented")

    # Not implemented yet
    def init_new_model(self) -> None:
        raise Exception("Not Implemented")

    # Not implemented yet
    def load_from_snapshot(self) -> None:
        raise Exception("Not Implemented")

    # 
    def find_optimal_parameters(self, input: numpy.array) -> numpy.array:
        allClusters: typing.List[numpy.array] = []
        allScores: typing.List[float] = []

        # Takes input, clusters them, then checks if clusters are correct
        # Assigns input to most optimal clusters afterwards
        for cluster in range(self.min_num_clusters, self.max_num_clusters):
            clustering: numpy.array = self.__cluster(input, cluster)

            allClusters.append(clustering)

            current_silhouette_score: float = self.calculate_silhouette_score(
                input, clustering
            )
            allScores.append(current_silhouette_score)

            if current_silhouette_score > self.max_score:
                self.max_score = current_silhouette_score
                self.optimal_clusters = cluster

    # Checks if num_cluster is actually set to catch errors, then calls actual clustering function
    def cluster(self, input_events: numpy.array, input_image: numpy.array) -> numpy.array:
        if self.num_clusters is None:
            raise Exception("Parameter num_cluster is None")

        return self.__cluster(input_events, self.num_clusters, input_image)

    # Not implemented yet
    def cluster_kalman(self, data: numpy):
        return
    
    # Uses sklearn Clustering function... with KMeans, not spectral clustering
    # https://scikit-learn.org/stable/modules/clustering.html#overview-of-clustering-methods
    def spectral_clustering(self,) -> SpectralClustering:
        return SpectralClustering(
            # predefined number of clusters
            n_clusters=self.num_clusters, 
            random_state=0,
            affinity='precomputed_nearest_neighbors',
            n_neighbors=self.num_neighbors, 
            # Use of KMeans as clustering method, available: 
            # KMeans, Affinity Propagation, MeanShift, SpectralClustering, Ward, Agglomerative Clustering
            # DBScan, OPTICS, BIRCH, Gaussian Mixture
            # maybe use DBScan, Optics or Spectral Clustering instead?
            assign_labels='kmeans',
            n_jobs=-1,
        )
    
    # uses sklearn nearest neighbors function to compute nearest neighbors
    # https://scikit-learn.org/stable/modules/neighbors.html
    def nearest_neighbors(self, events: numpy.array) -> NearestNeighbors:
        return kneighbors_graph(
            events,
            # num_neighbors is predefined
            n_neighbors=self.num_neighbors,
        )
    
    # uses sklearn.feature_extraction image function 
    # https://scikit-learn.org/stable/modules/feature_extraction.html
    def build_graph(self, event_image: numpy.array):
        # takes image as 2d-array as input (3d with color), extracts patches, 
        # creates weighting matrix which shows which samples (pixels) are connected\
        # img_to_graph returns pixel-to-pixel gradient connections, edges are weighted gradient values
        return image.img_to_graph(
            event_image,
        )
    
    # Central clustering function
    def __cluster(self, input_events: numpy.array, num_cluster: int, input_image: numpy.array) -> numpy.array:
        # Gets height and width from shape of input image
        image_height, image_width = input_image.shape[0], input_image.shape[1]
        
        #Reshapes array without changing values
        X = numpy.reshape(input_events, (-1, input_events.shape[-1]))
        
        mask = input_events.astype(bool)
        input_event = input_events.astype(float)
        
        
        tf_image = numpy.reshape(input_event, (input_event.shape[0], -1))
        
        print('X--->', X.shape, 'tf_image=--->', tf_image.shape, 'input_event--->', input_event.shape)
        
        # sklearn nearest neighbours function for input events array
        adjacency_matrix = self.nearest_neighbors(input_events)
        
        print('adjacency_matrix--->', adjacency_matrix.toarray().shape)
        
        # fit_predict performs spectral clustering, returns cluster labels
        spectral_labels: numpy = self.spectral_clustering().fit_predict(adjacency_matrix)
        # expand spectral labels array because...? 
        # In spectral_to_image, its always called as [i][0]
        spectral_labels = numpy.expand_dims(spectral_labels, axis=1)
        
        #Generates image array out of input events and its spectral labels
        output_labels: numpy.array = GSCEventMOD.convert_spectral_to_image(input_events, spectral_labels, image_height, image_width)
        
        # Generates bounding boxes around the clustered input with spectral labels
        detections = self.retrieve_bounding_boxes(output_labels, input_image)

        return detections

    # Pretty much just sklearn.metrics.silhouette_score()
    # Used to identify if sample is part of right cluster
    def calculate_silhouette_score(
        self, data: numpy.array, clustering: numpy.array) -> float:
        # from sklearn.metrics 
        # Computes and returns the mean Silhouette Coefficient of all samples (-1 = worst, 1 = best)
        # negative values = sample (probably) in wrong cluster 
        # Uses mean intra-cluster A distance and mean nearest-cluster distance B per sample
        # B is distance (sample <-> nearest cluster sample is not part of)
        return silhouette_score(data, clustering)
    

    # 
    def retrieve_bounding_boxes(self, output_labels: numpy.array, input_image: numpy) -> typing.Set[Detection]:
        detections = []
        # hererere? xD
        print('hererere image--->', type(input_image))
        print('output_lables---->', numpy.unique(output_labels))
        
        # 
        for label in range(self.num_clusters):

            # scipy.ndimage.find_objects() finds objects in a labeled array
            # useful for "isolating a volume of interest" in an array (or region of interest for 2D)
            slice_x, slice_y = ndimage.find_objects(output_labels==label)[0]
            
            print(slice_x, slice_y)

            # Region of Interest = ROI
            # takes only the segmented that ndimage.find_objects found interesting from original input image
            roi = input_image[slice_x, slice_y]
            
            print('roi--->', roi.shape)
            
            detections.append(roi)
            
        return detections
    

    # creates image-array with given width/height and assigns spectral values using the coordinates
    # from input events
    @staticmethod
    def convert_spectral_to_image(input_event: numpy, spectral_labels: numpy, height: int, width: int)-> numpy:
        # initializes empty "image" as two-dimensional array of unsigned integers with given width/height 
        output_image: numpy.array = numpy.full((height, width), -1).astype(numpy.uint8)
            
        # takes the x/y coordinates from event inputs and assigns a spectral label to them
        # given that not every "pixel" in the "image"-array has a spectral label,
        # those without input_event coordinate get skipped
        for i in range(spectral_labels.shape[0]):
            y, x = input_event[i][0], input_event[i][1]
            
            label = spectral_labels[i][0]
            
            print('label--->', label)
            
            output_image[x][y] = label
        
        return output_image
        
        
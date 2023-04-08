from src.Models.EventCamera import EventCamera
from sklearn.neighbors import kneighbors_graph, NearestNeighbors
from sklearn.metrics import silhouette_score
from sklearn.cluster import SpectralClustering
from sklearn.feature_extraction import image
import numpy
from scipy import ndimage
import pydantic
import typing
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

    def cluster(
        self, input_events: numpy.array, input_image: numpy.array
    ) -> numpy.array:
        if self.num_clusters is None:
            raise Exception("Parameter num_cluster is None")

        return self.__cluster(input_events, self.num_clusters, input_image)

    # Not implemented yet
    def cluster_kalman(self, data: numpy):
        return

    def spectral_clustering(
        self,
    ) -> SpectralClustering:
        """_summary_
        Returns:
            SpectralClustering: _description_
        """
        return SpectralClustering(
            n_clusters=self.num_clusters,
            random_state=0,
            affinity="precomputed_nearest_neighbors",
            n_neighbors=self.num_neighbors,
            assign_labels="kmeans",
            n_jobs=-1,
        )

    def nearest_neighbors(self, events: numpy.array) -> NearestNeighbors:
        return kneighbors_graph(
            events,
            # num_neighbors is predefined
            n_neighbors=self.num_neighbors,
        )
    def build_graph(self, event_image: numpy.array):
        # takes image as 2d-array as input (3d with color), extracts patches, 
        # creates weighting matrix which shows which samples (pixels) are connected\
        # img_to_graph returns pixel-to-pixel gradient connections, edges are weighted gradient values
        return image.img_to_graph(
            event_image,
        )

    def __cluster(
        self, input_events: numpy.array, num_cluster: int, input_image: numpy.array
    ) -> typing.List[numpy.array]:
        
        image_height, image_width = input_image.shape[0], input_image.shape[1]

        adjacency_matrix = self.nearest_neighbors(input_events)

        spectral_labels: numpy = self.spectral_clustering().fit_predict(
            adjacency_matrix
        )
        spectral_labels = numpy.expand_dims(spectral_labels, axis=1)

        output_labels: numpy.array = self.__convert_spectral_to_image(
            input_events, spectral_labels, image_height, image_width
        )

        detections, bounding_boxes = self.retrieve_bounding_boxes(
            output_labels, input_image
        )

        return detections, bounding_boxes

    # Pretty much just sklearn.metrics.silhouette_score()
    # Used to identify if sample is part of right cluster
    def calculate_silhouette_score(
        self, data: numpy.array, clustering: numpy.array
    ) -> float:
        return silhouette_score(data, clustering)

    def retrieve_bounding_boxes(
        self, output_labels: numpy.array, input_image: numpy
    ) -> typing.List[numpy.array]:
        detections = []
        bounding_boxes = []

        for label in range(self.num_clusters):
            slice_x, slice_y = ndimage.find_objects(output_labels == label)[0]

            width: int = slice_x.stop - slice_x.start
            height: int = slice_y.stop - slice_y.start

            roi = input_image[slice_x, slice_y]

            detections.append(roi)
            bounding_boxes.append([slice_x.start, slice_y.start, width, height])

        return detections, bounding_boxes

    def __convert_spectral_to_image(
        self, input_event: numpy, spectral_labels: numpy, height: int, width: int
    ) -> numpy:
        output_image: numpy.array = numpy.full((height, width), -1).astype(numpy.uint8)

        for i in range(spectral_labels.shape[0]):
            y, x = input_event[i][0], input_event[i][1]

            label = spectral_labels[i][0]

            output_image[x][y] = label

        return output_image

from src.Models.EventCamera import EventCamera
from sklearn.neighbors import kneighbors_graph
from sklearn.metrics import silhouette_score
from sklearn.cluster import SpectralClustering
import numpy
import abc
import typing


class GSCEventMOD(EventCamera):
    num_neighbors: int
    min_num_clusters: int
    max_num_clusters: int

    num_cluster: typing.Optional[int]

    max_score: float = float("infinity")
    optimal_clusters: int = 0

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def predict(self, input: numpy.array) -> None:
        raise NotImplemented
    
    def init_new_model(self) -> None:
        raise Exception('Not Implemented')
    
    def load_from_snapshot(self) -> None:
        raise Exception('Not Implemented')

    def find_optimal_parameters(self, input: numpy.array) -> numpy.array:

        allClusters: typing.List[numpy.array] = []
        allScores: typing.List[float] = []

        for cluster in range(self.min_num_clusters, self.max_num_clusters):
            
            clustering: numpy.array = self.__cluster(input, cluster)

            allClusters.append(clustering)

            current_silhouette_score: float = self.calculate_silhouette_score(input, clustering)
            allScores.append(current_silhouette_score)

            if current_silhouette_score > self.max_score:
                self.max_score = current_silhouette_score
                self.optimal_clusters = cluster
    
    def cluster(self, **data: typing.Any) -> numpy.array:
        if self.num_cluster is None:
            raise Exception('Parameter num_cluster is None')
         
        return self.__cluster(data, self.num_cluster)

    def __cluster(self, input: numpy.array, num_cluster: int) -> numpy.array:
        adjacencyMatrix: numpy.array = kneighbors_graph(
            X=input, 
            n_neighbors=self.num_neighbors
        )

        clustering: numpy.array = SpectralClustering(
                n_clusters=num_cluster,
                random_state=0,
                affinity='precomputed_nearest_neighbors',
                n_neighbors=self.num_neighbors,
                assign_labels='kmeans',
                n_jobs=-1
            ).fit_predict(adjacencyMatrix)
        
        return clustering
    
    def calculate_silhouette_score(self, data: numpy.array, clustering: numpy.array) -> float:
        return silhouette_score(data, clustering)
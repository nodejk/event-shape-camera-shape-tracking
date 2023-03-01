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

    max_score: float = float("infinity")
    optimal_clusters: int = 0

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def init_new_model(self) -> None:
        raise Exception('Not Implemented')
    
    def load_from_snapshot(self) -> None:
        raise Exception('Not Implemented')
    
    @abc.property
    def model_path(self) -> str:
        return ""
    
    def save_clusters_output(self, cluster: typing.List[numpy.array]) -> None:
        
        pass

    def find_optimal_parameters(self, data: numpy.array) -> numpy.array:
        adjacencyMatrix: numpy.array = kneighbors_graph(
            X=data, 
            n_neighbors=self.num_neighbors
        )

        allClusters: typing.List[numpy.array] = []
        allScores: typing.List[float] = []

        for cluster in range(self.min_num_clusters, self.max_num_clusters):
            
            clustering: numpy.array = SpectralClustering(
                n_clusters=cluster,
                random_state=0,
                affinity='precomputed_nearest_neighbors',
                n_neighbors=self.num_neighbors,
                assign_labels='kmeans',
                n_jobs=-1
            ).fit_predict(adjacencyMatrix)

            allClusters.append(clustering)

            current_silhouette_score: float = silhouette_score(data, clustering)
            allScores.append(current_silhouette_score)

            if current_silhouette_score > self.max_score:
                self.max_score = current_silhouette_score
                self.optimal_clusters = cluster

from src.Models.EventCamera import EventCamera
from sklearn.neighbors import kneighbors_graph
from sklearn.metrics import silhouette_score
from sklearn.cluster import SpectralClustering
import numpy
import pydantic
import typing
from src.Enums.ModelModeEnum import ModelModeEnum


class GSCEventMOD(EventCamera):
    num_neighbors: int
    mode: ModelModeEnum

    min_num_clusters: typing.Optional[int] = None
    max_num_clusters: typing.Optional[int] = None

    num_clusters: typing.Optional[int] = None

    max_score: float = float('infinity')
    optimal_clusters: int = 0

    @pydantic.root_validator()
    @classmethod
    def validate_mode(cls, field_values):
        mode: str = field_values['mode']

        if (mode == ModelModeEnum.FIND_OPTIMAL_CLUSTERS.value):
            if ('min_num_clusters' not in field_values or 'max_num_clusters' not in field_values):
                raise ValueError('Provide min_num_clusters and max_num_clusters to find the optimal number of clusters')
        else:
            if ('num_clusters' not in field_values):
                raise ValueError('Provide num_clusters in config in order to cluster')

        return field_values

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def predict(self, input: numpy.array) -> None:
        raise NotImplemented('predict not implemented')

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

    def cluster(self, data: numpy.array) -> numpy.array:
        if self.num_clusters is None:
            raise Exception('Parameter num_cluster is None')
         
        return self.__cluster(data, self.num_clusters)

    def __cluster(self, input: numpy.array, num_cluster: int) -> numpy.array:
        adjacencyMatrix: numpy.array = kneighbors_graph(
            X=input,
            n_neighbors=self.num_neighbors,
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

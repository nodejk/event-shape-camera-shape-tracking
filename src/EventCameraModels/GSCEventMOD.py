from src.Models.EventCameraModel import EventCameraModel
from sklearn.neighbors import kneighbors_graph
from sklearn.metrics import silhouette_score
from sklearn.cluster import SpectralClustering

class GSCEventMOD(EventCameraModel):
    numNeighbors: int
    minClusters: int
    maxClusters: int
    initMaxScore: int
    
    def __init__(self, configuration: dict) -> None:
        super().__init__(configuration)
        self.maxScore = self.initMaxScore
        self.optimalClusterNumbers = self.minClusters
        
    def initNewModel(self, initParameters) -> None:
        return super().initNewModel(initParameters)

    def cluster(self, data):
        adjacencyMatrix = kneighbors_graph(data, n_neighbors=self.numNeighbors)

        allClusters = []
        allScores = []

        for cluster in range(self.minClusters, self.maxClusters):
            clustering = SpectralClustering(
                n_clusters = cluster, 
                random_state = 0,                            
                affinity = 'precomputed_nearest_neighbors',
                n_neighbors = self.numNeighbors,
                assign_labels = 'kmeans',
                n_jobs = -1
            ).fit_predict(adjacencyMatrix)

            allClusters.append(clustering)
            
            currentSilhouetteScore = silhouette_score(data, clustering)
            allScores.append(currentSilhouetteScore)

            if currentSilhouetteScore > self.maxScore:
                self.maxScore = currentSilhouetteScore
                self.optimalClusterNumbers = cluster
            
            

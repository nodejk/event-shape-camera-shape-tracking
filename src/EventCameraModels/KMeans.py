from src.Models.EventCameraModel import EventCameraModel

class KMeans(EventCameraModel):
    numClusters: int
    testParameter: int
    testParameter2: str

    def __init__(self, configuration) -> None:
        super().__init__(configuration)
        
    def loadFromSnapShot(self, epochToRestoreFrom: str or int):
        pass
    
    def predict(self, xTrain):
        pass
    
    def initNewModel(self, initParameters) -> None:
        pass

    def fit(self, xTrain, yTrain):
        pass

    def cluster(self, data):
        pass
from src.Models.EventCameraModel import EventCameraModel

class KMeans(EventCameraModel):
    numClusters: int
    testParameter: int
    testParameter2: str

    def __init__(self, configuration) -> None:
        super().__init__(configuration)
        
    def loadFromSnapShot(self, epochToRestoreFrom: str or int):
        print("here")
        return super().loadFromSnapShot(epochToRestoreFrom)
    
    def predict(self, xTrain):
        print("predict")
    
    def initNewModel(self, initParameters) -> None:
        print("new model")

    def fit(self, xTrain, yTrain):
        print(self.numClusters)
        print(self.testParameter)
        print(self.testParameter2)
        print("fit")
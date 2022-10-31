from abc import abstractmethod

class EventCameraModel():
    
    def __init__(self, modelName: str) -> None:
        self.modelName: str = modelName

    @abstractmethod
    def fit(self, xTrain, yTrain):
        pass

    @abstractmethod
    def predict(self, xTrain):
        pass

from abc import abstractmethod
from typing import List
from src.Models.AbstractModule import AbstractModule

'''
    Initialize required parameters inside class as attributes.
'''
class EventCameraModel(AbstractModule):
    modelName: str

    def __init__(self, configuration: dict) -> None:
        self.modelName = self.toPascalCase(self.__class__.__name__)
        super().__init__(self.getRequiredParameters(), configuration)
        self.setParameters()

    @abstractmethod
    def fit(self, xTrain, yTrain):
        raise NotImplementedError

    @abstractmethod
    def predict(self, xTrain):
        raise NotImplementedError
    
    @abstractmethod
    def loadFromSnapShot(self, epochToRestoreFrom: str):
        raise NotImplementedError

    @abstractmethod
    def initNewModel(self, initParameters) -> None:
        raise NotImplementedError

    def setParameters(self):
        for key in self.getRequiredParameters():
            setattr(self.__class__, key, self.requiredParametersDict[key])
    
    def getRequiredParameters(self) -> List[str]:
        return [a for a in self.__class__.__annotations__.keys()]
        
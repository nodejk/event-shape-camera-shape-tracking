from abc import abstractmethod
from src.Models.AbstractModule import AbstractModule
from typing import List

class DataTransformerModel(AbstractModule):
    modelName: str

    def __init__(self, configuration: dict) -> None:
        self.modelName = self.toPascalCase(self.__class__.__name__)
        super().__init__(self.getRequiredParameters(), configuration)
        self.setParameters()

    @abstractmethod
    def transform() -> None:
        pass
    
    def setParameters(self):
        for key in self.getRequiredParameters():
            setattr(self.__class__, key, self.requiredParametersDict[key])
    
    def getRequiredParameters(self) -> List[str]:
        return [a for a in self.__class__.__annotations__.keys()]

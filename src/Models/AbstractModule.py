from abc import ABCMeta
from src.utils.string import camelCase, pascalCase

class AbstractModule(metaclass=ABCMeta):
    requiredParametersList: list
    requiredParametersDict: dict
    
    def __init__(self, requiredParametersList: list, configuration: dict) -> None:
        self.requiredParametersList = requiredParametersList
        self.requiredParametersDict = self.loadParametersFromConfiguration(configuration)
        self.checkIfRequiredParametersProvided()

    def checkIfRequiredParametersProvided(self):
        if (self.requiredParametersList == None):
            raise Exception('Required Parameters not found. Please provide requiredParametersList in ' + self.__class__.__name__)
    
    def loadParametersFromConfiguration(self, configuration: dict) -> dict:
        requiredParametersDict = {}

        for key in self.requiredParametersList:
            try:
                requiredParametersDict[key] = configuration[key]
            except:
                raise Exception('Required key {} not found in configuration json. Please check config.json for {}'.format(key, self.__class__.__name__))

        return requiredParametersDict
    
    def toCamelCase(self, input: str) -> str:
        return camelCase(input)
    
    def toPascalCase(self, input: str) -> str:
        return pascalCase(input)
import json
from typing import List
import os
from dataclasses import dataclass

@dataclass
class ModelRestoreParameters:
    iterationToRestoreFrom: int
    modelPath: str

@dataclass
class ModelParamtersConfig:
    modelName: str
    restoreModel: bool
    parameters: dict
    restoreModelParameters: ModelRestoreParameters

@dataclass
class DataConfig:
    name: str
    parameters: dict

@dataclass
class TrainValidationTestSplit:
    trainPercentage: float
    validationPercentage: float
    testPercentage: float

@dataclass
class DataProcessorConfig:
    processedDataPath: str
    usePreprocessedData: bool
    dataInputPath: str
    processedDataSavedPath: str
    trainValidationTestSplit: TrainValidationTestSplit
    steps: List[DataConfig]

@dataclass
class ConfigurationProvider:
    batchSize: int
    epochs: int
    modelSavePath: str
    dataInputPath: str
    modelParameters: ModelParamtersConfig
    dataProcessors: DataProcessorConfig
    dataTransformers: List[DataConfig]
    
    def __init__(self):
        configurationProvided = None
        with open(self.getFilePath()) as f:
            configurationProvided = self.changeKeysToCamel(json.load(f))
        
        self.modelParameters = ModelParamtersConfig(**configurationProvided['modelParameters'])
        self.modelParameters.restoreModelParameters = ModelRestoreParameters(**configurationProvided['modelParameters']['restoreModelParameters'])
        
        self.dataProcessors = DataProcessorConfig(**configurationProvided['dataProcessors'])
        self.dataProcessors.trainValidationTestSplit = TrainValidationTestSplit(**configurationProvided['dataProcessors']['trainValidationTestSplit'])
        self.dataProcessors.steps = [DataConfig(**processor) for processor in configurationProvided['dataProcessors']['steps']]
        
        self.dataTransformers = [DataConfig(**transformer) for transformer in configurationProvided['dataTransformers']]
        self.epochs = configurationProvided['epochs']
        self.batchSize = configurationProvided['batchSize']

    def checkConfiguration():
        pass

    def kebabToCamelCase(self, parameterName: str) -> str:
        components = parameterName.split('-')
        return components[0] + ''.join(x.title() for x in components[1:])

    def changeKeysToCamel(self, obj) -> dict:
        if isinstance(obj, (str, int, float)):
            return obj
        if isinstance(obj, dict):
            new = obj.__class__()
            for k, v in obj.items():
                new[self.kebabToCamelCase(k)] = self.changeKeysToCamel(v)
        elif isinstance(obj, (list, set, tuple)):
            new = obj.__class__(self.changeKeysToCamel(v) for v in obj)
        else:
            return obj
        return new
    
    def getFilePath(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath('__file__')), 'config.json')


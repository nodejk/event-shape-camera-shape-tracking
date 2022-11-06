from abc import abstractmethod
from glob import glob
from typing import List
from src.Models.DataProcessorModel import DataProcessorModel
from src.Models.ConfigurationProvider import ConfigurationProvider
from src.Models.DataTransformerModel import DataTransformerModel
from src.Models.EventCameraModel import EventCameraModel
import importlib
from src.utils.string import pascalCase

class ContextProviderModel():
    _iteration: int
    _configuration: ConfigurationProvider
    _model: EventCameraModel
    _dataProcessors: List[DataProcessorModel]
    _dataTransformers: List[DataTransformerModel]
    
    modelPath: str = "EventCameraModels"
    dataProcessorPath: str = "DataProcessors"
    dataTransformersPath: str = "DataTransformers"
    
    def __init__(self) -> None:
        self._configuration = ConfigurationProvider()
        self._dataTransformers = []
        self._dataProcessors = []

        print(self._configuration.batchSize)
        self.loadModel()
        self.setDataTransformerInstances()
        self.setDataProcessorInstances()

        if self._configuration.dataProcessors.usePreprocessedData == False:
            self.preProcessData()

    def checkIfConfigurationPossible(self) -> bool:
        pass

    def checkIfModelExists(self) -> bool:
        pass

    def openFile(self):
        return "123"

    def preProcessData(self) -> bool:
        print('Processing Data...')
        inputDataPath = self._configuration.dataProcessors.dataInputPath

        files = glob(inputDataPath + '/*')
        print(files)
        if len(files) == 0:
            raise Exception('No files found in directory {}'.format(inputDataPath))

        for file in files:
            lastOutput = None
            for index, dataProcessor in enumerate(self._dataProcessors):
                if index == 0:
                    output = self.openFile()
                lastOutput = dataProcessor.processData(output)

                print("index-->", output)

    def run(self) -> None:
        pass

    def loadModel(self) -> None:
        modelName = self._configuration.modelParameters.modelName
        if (self._configuration.modelParameters.restoreModel == True):
            self._model = self.getInstance(self.modelPath, modelName, self._configuration.modelParameters.parameters)
            self._iteration = self._configuration.modelParameters.restoreModelParameters.iterationToRestoreFrom
        else:
            self._model = self.getInstance(self.modelPath, modelName, self._configuration.modelParameters.parameters)
            self._iteration = 0
    
    @abstractmethod
    def snapShotModel() -> None:
        pass

    def toPascalCase(self, modelName: str) -> str:
        return pascalCase(modelName)
    
    def getInstance(self, modelPath: str, modelName: str, configuration: dict,):
        pascalModelName: str = self.toPascalCase(modelName)

        importModule = importlib.import_module('src.{}.'.format(modelPath) + pascalModelName)
        modelInstance = getattr(importModule, pascalModelName)
        model = modelInstance(configuration)
        
        if (type(model) is not modelInstance):
            raise Exception('Model provided does not implement {}. Please check the model: {}'.format(modelPath, model.__class__.__name__))
        
        return model
    
    def setDataTransformerInstances(self) -> str:
        for dataTransformer in self._configuration.dataTransformers:
            dataTransformerModel = self.getInstance(self.dataTransformersPath, dataTransformer.name, dataTransformer.parameters)
            self._dataTransformers.append(dataTransformerModel)
    
    def setDataProcessorInstances(self) -> str:
        for dataProcessorStep in self._configuration.dataProcessors.steps:
            dataProcessorModel = self.getInstance(self.dataProcessorPath, dataProcessorStep.name, dataProcessorStep.parameters)
            self._dataProcessors.append(dataProcessorModel)


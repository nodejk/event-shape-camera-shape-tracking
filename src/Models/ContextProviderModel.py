from abc import abstractmethod
from glob import glob
from typing import List
from src.Models.DataProcessorModel import DataProcessorModel
from src.Models.ConfigurationProvider import ConfigurationProvider
from src.Models.DataTransformerModel import DataTransformerModel
from src.Models.EventCameraModel import EventCameraModel
import importlib
from src.utils.string import pascalCase
from src.Types.PipelineEnum import PipelineEnum
from datetime import datetime
import os

class ContextProviderModel():
    _iteration: int
    _configuration: ConfigurationProvider
    _model: EventCameraModel
    _dataProcessors: List[DataProcessorModel]
    _dataTransformers: List[DataTransformerModel]
    
    modelPath: str = "EventCameraModels"
    dataProcessorPath: str = "DataProcessors"
    dataTransformersPath: str = "DataTransformers"

    saveProcessedDataPath: str
    saveMachineLearningExperimentsPath: str
    
    def __init__(self) -> None:
        self._configuration = ConfigurationProvider()
        self._dataTransformers = []
        self._dataProcessors = []

        self.loadModel()
        self.setDataTransformerInstances()
        self.setDataProcessorInstances()
        self.saveProcessedDataPath = 'preProcessedData' + '/' + self.currentTimeStamp()
        self.saveMachineLearningExperimentsPath = 'machineLearningExperiments' + '/' + self.currentTimeStamp()
        
        self.initPipeline()
    
    def initPipeline(self, ) -> None:
        if (self._configuration.pipelineType == PipelineEnum.PROCESS_DATA): self.preProcessData()
        if (self._configuration.pipelineType == PipelineEnum.TRAIN_MODEL): self.trainModel()

    def trainModel(self, ) -> None:
        print('Training Machine Learning Model.....')

        if self._configuration.modelParameters.restoreModel == True:
            pass
        else:
            pass        

        pass

    def checkIfConfigurationPossible(self) -> bool:
        pass

    def checkIfModelExists(self) -> bool:
        pass
    
    @abstractmethod
    def openFile(self, filePath):
        raise Exception('Open file not implemented.')

    @abstractmethod
    def writeProcessedData(self, dataToSave, fileName: str):
        raise Exception('Write file not implemented')

    def currentTimeStamp(self, ) -> str:
        dateTimeObj = datetime.now()
        return dateTimeObj.year + '_' + dateTimeObj.month + '_' + dateTimeObj.day + '_' + dateTimeObj.hour + '_' + dateTimeObj.minute + '_' + dateTimeObj.second

    def preProcessData(self) -> bool:
        print('Processing Data...')
        inputDataPath = self._configuration.dataProcessors.dataInputPath

        files = glob(inputDataPath + '/*')

        if len(files) == 0:
            raise Exception('No files found in directory {}'.format(inputDataPath))

        for filePath in files:
            output = self.openFile(filePath)
            _, fileName = os.path.split(filePath)

            for dataProcessor in self._dataProcessors:
                output = dataProcessor.processData(output)
            self.writeProcessedData(output, fileName)

    def run(self) -> None:
        pass
    
    def saveProcessedData(self) -> List[str]:
        self._configuration.dataProcessors.processedDataPath + ''

    def loadModel(self) -> None:
        modelName = self._configuration.modelParameters.modelName
        if (self._configuration.modelParameters.restoreModel == True):
            self._model = self.getInstance(self.modelPath, modelName, self._configuration.modelParameters.parameters)
            self._model.loadFromSnapShot(self._configuration.modelParameters.restoreModelParameters.iterationToRestoreFrom)
            self._iteration = self._configuration.modelParameters.restoreModelParameters.iterationToRestoreFrom
        else:
            self._model = self.getInstance(self.modelPath, modelName, self._configuration.modelParameters.parameters)
            self._iteration = 0
    
    @abstractmethod
    def snapShotModel() -> None:
        pass

    def toPascalCase(self, modelName: str) -> str:
        return pascalCase(modelName)
    
    def getInstance(self, modelPath: str, modelName: str, configuration: dict,) -> EventCameraModel:
        pascalModelName: str = self.toPascalCase(modelName)

        importModule = importlib.import_module('src.{}.'.format(modelPath) + pascalModelName)
        modelInstance = getattr(importModule, pascalModelName)
        model = modelInstance(configuration)
        
        if (type(model) is not modelInstance):
            raise Exception('Model provided does not implement {}. Please check the model: {}'.format(modelPath, model.__class__.__name__))
        
        return model
    
    def setDataTransformerInstances(self) -> None:
        for dataTransformer in self._configuration.dataTransformers:
            dataTransformerModel = self.getInstance(self.dataTransformersPath, dataTransformer.name, dataTransformer.parameters)
            self._dataTransformers.append(dataTransformerModel)
    
    def setDataProcessorInstances(self) -> None:
        for dataProcessorStep in self._configuration.dataProcessors.steps:
            dataProcessorModel = self.getInstance(self.dataProcessorPath, dataProcessorStep.name, dataProcessorStep.parameters)
            self._dataProcessors.append(dataProcessorModel)

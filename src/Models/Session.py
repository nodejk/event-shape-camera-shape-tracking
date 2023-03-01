from glob import glob
import typing
from src.Models.Configuration import Configuration
import importlib
from src.utils.string import pascalCase
from pydantic.tools import parse_obj_as
from datetime import datetime
import json
import os

class Session:
    configuration: Configuration
    
    def __init__(self, config_path: str) -> None:
        if (config_path is None):
            raise Exception('Configuration File Not Provided')
        
        with open(config_path) as file:
            print('Loading the configuration...')
            json_configuration: dict[typing.Any, typing.Any] = json.loads(file.read())

            self.configuration = Configuration(**json_configuration)

        pipeline = importlib.import_module(f'src.{self.configuration.model}').Pipeline(self.configuration)
        
        
        # self._dataTransformers = []
        # self._dataProcessors = []

        # self.loadModel()
        # self.setDataTransformerInstances()
        # self.setDataProcessorInstances()
        # self.saveProcessedDataPath = 'preProcessedData' + '/' + self.currentTimeStamp()
        # self.saveMachineLearningExperimentsPath = 'machineLearningExperiments' + '/' + self.currentTimeStamp()
        
        # self.initPipeline()
    
    # def initPipeline(self, ) -> None:
    #     # if (self._configuration.pipelineType == PipelineEnum.PROCESS_DATA): self.preprocess_data()
    #     # if (self._configuration.pipelineType == PipelineEnum.TRAIN_MODEL): self.trainModel()

    #     pass
    
    # @abstractmethod
    # def openFile(self, filePath):
    #     raise Exception('Open file not implemented.')

    # @abstractmethod
    # def writeProcessedData(self, dataToSave, fileName: str):
    #     raise Exception('Write file not implemented')

    # def currentTimeStamp(self, ) -> str:
    #     dateTimeObj = datetime.now()
    #     return dateTimeObj.year + '_' + dateTimeObj.month + '_' + dateTimeObj.day + '_' + dateTimeObj.hour + '_' + dateTimeObj.minute + '_' + dateTimeObj.second

    # def preprocess_data(self) -> bool:
    #     print('Processing Data...')
    #     inputDataPath = self._configuration.dataProcessors.dataInputPath

    #     files = glob(inputDataPath + '/*')

    #     if len(files) == 0:
    #         raise Exception('No files found in directory {}'.format(inputDataPath))

    #     for filePath in files:
    #         output = self.openFile(filePath)
    #         _, fileName = os.path.split(filePath)

    #         for dataProcessor in self._dataProcessors:
    #             output = dataProcessor.process_data(output)
    #         self.writeProcessedData(output, fileName)

    # def run(self) -> None:
    #     pass
    
    # def saveProcessedData(self) -> List[str]:
    #     self._configuration.dataProcessors.processedDataPath + ''

    # def loadModel(self) -> None:
    #     modelName = self._configuration.modelParameters.modelName
    #     if (self._configuration.modelParameters.restoreModel == True):
    #         self._model = self.getInstance(self.modelPath, modelName, self._configuration.modelParameters.parameters)
    #         self._model.loadFromSnapShot(self._configuration.modelParameters.restoreModelParameters.iterationToRestoreFrom)
    #         self._iteration = self._configuration.modelParameters.restoreModelParameters.iterationToRestoreFrom
    #     else:
    #         self._model = self.getInstance(self.modelPath, modelName, self._configuration.modelParameters.parameters)
    #         self._iteration = 0
    
    # @abstractmethod
    # def snapShotModel() -> None:
    #     pass

    # def toPascalCase(self, modelName: str) -> str:
    #     return pascalCase(modelName)
    
    # def getInstance(self, modelPath: str, modelName: str, configuration: dict,) -> EventCameraModel:
    #     pascalModelName: str = self.toPascalCase(modelName)

    #     importModule = importlib.import_module('src.{}.'.format(modelPath) + pascalModelName)
    #     modelInstance = getattr(importModule, pascalModelName)
    #     model = modelInstance(configuration)
        
    #     if (type(model) is not modelInstance):
    #         raise Exception('Model provided does not implement {}. Please check the model: {}'.format(modelPath, model.__class__.__name__))
        
    #     return model
    
    # def setDataTransformerInstances(self) -> None:
    #     for dataTransformer in self._configuration.dataTransformers:
    #         dataTransformerModel = self.getInstance(self.dataTransformersPath, dataTransformer.name, dataTransformer.parameters)
    #         self._dataTransformers.append(dataTransformerModel)
    
    # def setDataProcessorInstances(self) -> None:
    #     for dataProcessorStep in self._configuration.dataProcessors.steps:
    #         dataProcessorModel = self.getInstance(self.dataProcessorPath, dataProcessorStep.name, dataProcessorStep.parameters)
    #         self._dataProcessors.append(dataProcessorModel)

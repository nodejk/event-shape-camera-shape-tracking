from abc import abc, abstractmethod
from src.Models.DataProcessorModel import DataProcessorModel

class ContextProviderModel(abc):
    trainingParameters: list(str)
    dataProcessingParameter: list(str)
    modelParameters: list(str)

    def __init__(self, dataProcessor: DataProcessorModel, config: dict) -> None:
        self.dataProcessor = dataProcessor
        self.config: dict = config

        self.trainingParameters = [
            'batch-size',       # batch size (number, required)
            'epochs',           # epochs to train the model (number, required)
            'learning-rate',    # learning rate of the model (number, required)
        ]

        self.dataProcessingParameter = [
            'data-path',         # data-path for pre-processed data (string, required)
            'data-processor',    # data processor path if data is not pre-processed (string, required)
            'data-transformer',  # path of data transformer (string, required)
        ]

        self.modelParameters = [
            'model-name',           # name of the model (string, required)
            'restore-model',        # restore last model from training (boolean, required)
            'restore-model-path',   # restoration model path (string, required if restore-model is true)
        ]

    def checkIfConfigurationPossible(self) -> bool:
        pass

    def checkIfModelExists(self) -> bool:
        pass

    def run(self) -> None:
        pass

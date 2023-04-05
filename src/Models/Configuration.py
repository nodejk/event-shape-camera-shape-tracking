from typing import List
import os
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
import typing


@dataclass
class ModelRestoreParameters:
    iteration_to_restore_from: int
    model_path: str


@dataclass
class ModelParamtersConfig:
    restore_model: bool
    num_grouped_events: int
    parameters: dict


@dataclass
class DataConfig:
    name: str
    parameters: dict


@dataclass
class TrainValidationTestSplit:
    train_percentage: float
    validation_percentage: float
    test_percentage: float


@dataclass
class DataProcessorConfig:
    data_input_path: str
    class_balanced_split: str
    train_validation_test_split: TrainValidationTestSplit
    steps: List[DataConfig]


@dataclass
class AedatFileReaderConfig:
    path: str


@dataclass
class DetectionGSCEventStreamerConfig:
    address: int
    port: str


class Configuration(BaseModel):
    model: str
    pipeline_type: str
    aedat_file_reader_config: AedatFileReaderConfig
    detection_gsc_event_reader_config: typing.Optional[DetectionGSCEventStreamerConfig]
    visualize: bool
    model_parameters: ModelParamtersConfig
    data_processors: DataProcessorConfig
    data_transformers: List[DataConfig]

    # def __init__(self):
    #     configurationProvided = None
    #     # with open(self.getFilePath()) as f:
    #     configurationProvided = self.changeKeysToCamel(json.load(f))

    # self.modelParameters = ModelParamtersConfig(**configurationProvided['modelParameters'])
    # self.modelParameters.restoreModelParameters = ModelRestoreParameters(**configurationProvided['modelParameters']['restoreModelParameters'])

    # self.dataProcessors = DataProcessorConfig(**configurationProvided['dataProcessors'])
    # self.dataProcessors.trainValidationTestSplit = TrainValidationTestSplit(**configurationProvided['dataProcessors']['trainValidationTestSplit'])
    # self.dataProcessors.steps = [DataConfig(**processor) for processor in configurationProvided['dataProcessors']['steps']]

    # self.dataTransformers = [DataConfig(**transformer) for transformer in configurationProvided['dataTransformers']]
    # self.epochs = configurationProvided['epochs']
    # self.batchSize = configurationProvided['batchSize']

    def kebabToCamelCase(self, parameterName: str) -> str:
        components = parameterName.split("-")
        return components[0] + "".join(x.title() for x in components[1:])

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
        return os.path.join(
            os.path.dirname(os.path.realpath("__file__")), "config.json"
        )

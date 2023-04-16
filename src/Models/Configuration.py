from typing import List
import os
from pydantic.dataclasses import dataclass
import pydantic
import typing


@dataclass
class ModelRestoreParameters:
    iteration_to_restore_from: int
    model_path: str


@dataclass
class ModelParametersConfig:
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
    steps: List[DataConfig]


@dataclass
class DataTransformerConfig:
    steps: List[DataConfig]


@dataclass
class AedatFileReaderConfig:
    path: str


@dataclass
class DetectionGSCEventStreamerConfig:
    address: int
    port: str


class Configuration(pydantic.BaseModel):
    model: str
    pipeline_type: str
    aedat_file_reader_config: AedatFileReaderConfig
    detection_gsc_event_reader_config: typing.Optional[DetectionGSCEventStreamerConfig]
    visualize: bool
    model_parameters: ModelParametersConfig
    data_processors: DataProcessorConfig
    event_data_processors: DataProcessorConfig
    data_transformers: DataTransformerConfig

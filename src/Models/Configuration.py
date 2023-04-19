from typing import List
from pydantic.dataclasses import dataclass
import pydantic
import typing


@dataclass
class ModelRestoreParameters:
    iteration_to_restore_from: int
    model_path: str


@dataclass
class ModelParametersConfig:
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
class EventInputConfig:
    source_type: str
    parameters: typing.Dict[str, str]


@dataclass
class DetectionGSCEventStreamerConfig:
    address: int
    port: str


@dataclass
class ModelOutputConfig:
    save: bool


class Configuration(pydantic.BaseModel):
    model: str
    pipeline_type: str
    events_input: EventInputConfig
    model_output: ModelOutputConfig
    detection_gsc_event_reader_config: typing.Optional[DetectionGSCEventStreamerConfig]
    visualize: bool
    model_parameters: ModelParametersConfig
    data_processors: DataProcessorConfig
    event_data_processors: DataProcessorConfig
    data_transformers: DataTransformerConfig

    class Config:
        use_enum_values = True

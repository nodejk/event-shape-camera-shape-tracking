from enum import Enum


class PipelineEnum(Enum):
    REAL_TIME: str= 'real-time'
    STEP_PREDICTION: str = 'step'

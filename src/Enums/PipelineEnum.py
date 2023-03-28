from enum import Enum


class PipelineEnum(Enum):
    REAL_TIME: str = "real-time"
    STEP_PREDICTION: str = "step-prediction"
    FIND_OPTIMAL_PARAMETERS: str = "find-optimal-params"

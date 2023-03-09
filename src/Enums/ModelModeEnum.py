from enum import Enum

class ModelModeEnum(str, Enum):
    FIND_OPTIMAL_CLUSTERS: str = 'find-optimal-clusters'
    CLUSTER: str = 'cluster'
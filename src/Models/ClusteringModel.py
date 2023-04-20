import abc
import pydantic
import numpy
import typing


class ClusteringModel(pydantic.BaseModel):
    model_name: str

    @abc.abstractmethod
    def find_optimal_parameters(self, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def load_from_snapshot(self, session_to_restore_from: str) -> None:
        raise NotImplementedError

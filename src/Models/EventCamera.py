import abc
import pydantic
import numpy
import typing


class EventCamera(pydantic.BaseModel):
    model_name: str

    @abc.abstractmethod
    def predict(self, input: numpy.array) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def find_optimal_parameters(self, input: numpy.array) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def cluster(self, **data: typing.Any) -> numpy.array:
        raise NotImplementedError
    
    @abc.abstractmethod
    def load_from_snapshot(self, epochToRestoreFrom: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def init_new_model(self, initParameters) -> None:
        raise NotImplementedError
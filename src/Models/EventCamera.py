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
    def cluster(self, **kwargs: typing.Any) -> numpy.array:
        raise NotImplementedError

    @abc.abstractmethod
    def load_from_snapshot(self, epoch_to_restore_from: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def init_new_model(self, init_parameters) -> None:
        raise NotImplementedError

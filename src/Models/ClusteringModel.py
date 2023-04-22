import abc
import pydantic
import numpy
import typing

from stonesoup.types.sensordata import ImageFrame


class ClusteringModel(pydantic.BaseModel):
    model_name: str

    @abc.abstractmethod
    def load_from_snapshot(self, session_to_restore_from: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def cluster(self, input_events: numpy.array, image_frame: ImageFrame) -> typing.Any:
        raise NotImplementedError

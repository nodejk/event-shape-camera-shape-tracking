import abc
import numpy
import pydantic


class BaseDataTransformer(pydantic.BaseModel):
    name: str

    @abc.abstractmethod
    def transform(self, input_data: numpy.array) -> numpy.ndarray:
        raise Exception("Method transform not implemented for {}".format(self.name))

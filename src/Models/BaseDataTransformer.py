import abc
import numpy
import pydantic


class BaseDataTransformer(pydantic.BaseModel):
    name: str

    @abc.abstractmethod
    def transform(self, input: numpy.array) -> None:
        raise Exception("Method transform not implemented for {}".format(self.name))

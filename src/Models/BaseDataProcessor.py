import abc
import pydantic
import numpy


class BaseDataProcessor(pydantic.BaseModel):
    name: str

    @abc.abstractmethod
    def process_data(self, input_image: numpy.array) -> numpy.ndarray:
        raise Exception(
            "Method process_data not implemented for data processor model: {}".format(
                self.name
            )
        )

    class Config:
        arbitrary_types_allowed = True

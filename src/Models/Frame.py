import numpy
import pydantic
import pickle
import typing
import dv


class Frame(pydantic.BaseModel):
    path: str

    image: numpy.array = None
    event: dv.Event = None

    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)

        with open(self.path, 'rb') as file_pointer:
            loaded_dictionary = pickle.load(file_pointer)
            self.image = loaded_dictionary['image']
            self.event = loaded_dictionary['events']

    class Config:
        allow_arbitary_types = True

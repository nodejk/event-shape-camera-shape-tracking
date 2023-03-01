import pydantic
import typing
import numpy


class KalmanFilter(pydantic.BaseModel):
    dt: int

    acc_x: float
    acc_y: float

    noise_magnitude: float

    std_x: float
    std_y: float

    control_input_var: numpy.array
    
    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)

        self.control_input_var = numpy.matrix([[self.acc_x], [self.acc_y]]) 

    @staticmethod
    def get_initial_state() -> numpy.matrix:
        return numpy.matrix

    class Config:
        arbitrary_types_allowed = True        
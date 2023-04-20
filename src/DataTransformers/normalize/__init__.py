from src.Models.BaseDataTransformer import BaseDataTransformer
import numpy


class DataTransformer(BaseDataTransformer):
    output_range_min: int
    output_range_max: int

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def transform(self, input_image: numpy.ndarray) -> numpy.ndarray:
        return input_image

from src.Models.BaseDataProcessor import BaseDataProcessor
import numpy


class DataProcessor(BaseDataProcessor):
    x_left: int
    x_right: int
    y_top: int
    y_bottom: int

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def process_data(self, input_image: numpy.array):
        return input_image[self.y_top: self.y_bottom, self.x_left: self.x_right]

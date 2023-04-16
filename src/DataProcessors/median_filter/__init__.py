from src.Models.BaseDataProcessor import BaseDataProcessor
import numpy
import scipy


class DataProcessor(BaseDataProcessor):
    size: int

    def process_data(self, input_image: numpy.array) -> numpy.ndarray:
        return scipy.ndimage.median_filter(input_image, self.size)

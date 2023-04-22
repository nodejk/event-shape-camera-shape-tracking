import cv2 as cv
import numpy


class Visualizer:
    @staticmethod
    def visualize(image: numpy.ndarray, window_name: str) -> None:
        cv.imshow(window_name, image)
        cv.waitKey(1)

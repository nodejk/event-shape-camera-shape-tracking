import cv2 as cv
import numpy


class Visualizer:
    @staticmethod
    def visualize(input: numpy.array, window_name: str) -> None:
        cv.imshow(window_name, input)
        
        cv.waitKey(0)
        # if cv.waitKey(10) == 13:
        #     return

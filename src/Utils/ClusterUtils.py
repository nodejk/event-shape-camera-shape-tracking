import numpy
import typing


class ClusterUtils:
    @staticmethod
    def convert_spectral_to_image(
        input_event: numpy.ndarray, spectral_labels: numpy.ndarray, height: int, width: int
    ) -> numpy.ndarray:
        output_image: numpy.ndarray = numpy.full((height, width), -1).astype(numpy.uint8)

        for i in range(spectral_labels.shape[0]):
            y, x = input_event[i][1], input_event[i][0]

            label = spectral_labels[i][0]

            output_image[x][y] = label

        return output_image

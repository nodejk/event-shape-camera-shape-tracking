import numpy
import typing
import scipy
from sklearn.neighbors import kneighbors_graph, NearestNeighbors
from stonesoup.types.detection import Detection
from stonesoup.types.sensordata import ImageFrame


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

    @staticmethod
    def get_nn_adjacency_matrix(events: numpy.ndarray, num_neighbors: int) -> NearestNeighbors:
        return kneighbors_graph(
            events,
            n_neighbors=num_neighbors,
        )

    @staticmethod
    def retrieve_bounding_boxes(
        num_clusters: int, output_labels: numpy.ndarray, image_frame: ImageFrame
    ) -> typing.Tuple[typing.List[numpy.ndarray], typing.Set[Detection]]:
        detections: typing.Set[Detection] = set()
        bounding_boxes: typing.List[numpy.ndarray] = []

        for label in range(num_clusters):
            slice_x, slice_y = scipy.ndimage.find_objects(output_labels == label)[0]

            width: int = slice_x.stop - slice_x.start
            height: int = slice_y.stop - slice_y.start

            roi = image_frame.pixels[slice_x, slice_y]

            bounding_boxes.append(roi)
            detection: Detection = Detection(
                [slice_x.start, slice_y.start, width, height],
                timestamp=image_frame.timestamp,
                metadata={
                    "object_id": label,
                },
            )

            detections.add(detection)

        return bounding_boxes, detections

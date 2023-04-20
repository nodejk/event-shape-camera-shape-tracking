import functools

from src.Models.ClusteringModel import ClusteringModel
from sklearn.neighbors import kneighbors_graph, NearestNeighbors
from sklearn.metrics import silhouette_score
from sklearn.cluster import SpectralClustering
import numpy
from scipy import ndimage
from stonesoup.types.sensordata import ImageFrame
import pydantic
import typing
from src.Enums.ModelModeEnum import ModelModeEnum
from stonesoup.types.detection import Detection
from src.Utils.ClusterUtils import ClusterUtils


class GSCEventMOD(ClusteringModel):
    model_name = "GSC_EVENT_MOD"

    num_neighbors: int
    mode: ModelModeEnum

    min_num_clusters: typing.Optional[int] = None
    max_num_clusters: typing.Optional[int] = None

    num_clusters: typing.Optional[int] = None

    max_score: float = float("infinity")
    optimal_clusters: int = 0

    @pydantic.root_validator()
    @classmethod
    def validate_mode(cls, field_values):
        print(field_values)
        mode: str = field_values["mode"]

        if mode == ModelModeEnum.FIND_OPTIMAL_CLUSTERS.value:
            if (
                "min_num_clusters" not in field_values
                or "max_num_clusters" not in field_values
            ):
                raise ValueError(
                    "Provide min_num_clusters and max_num_clusters to find the optimal number of clusters"
                )
        else:
            if "num_clusters" not in field_values:
                raise ValueError("Provide num_clusters in config in order to cluster")

        return field_values

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def load_from_snapshot(self, session_to_restore_from: str) -> None:
        raise Exception("Not Implemented")

    def find_optimal_parameters(self, events_input: numpy.ndarray) -> None:
        all_clusters: typing.List[numpy.array] = []
        all_scores: typing.List[float] = []

        for cluster in range(self.min_num_clusters, self.max_num_clusters):
            clustering: numpy.array = self.__cluster(events_input, cluster)

            all_clusters.append(clustering)

            current_silhouette_score: float = self.calculate_silhouette_score(
                events_input, clustering
            )
            all_scores.append(current_silhouette_score)

            if current_silhouette_score > self.max_score:
                self.max_score = current_silhouette_score
                self.optimal_clusters = cluster

    def cluster(
        self, input_events: numpy.array, image_frame: ImageFrame
    ) -> typing.Tuple[typing.List[numpy.ndarray], typing.Set[Detection]]:
        if self.num_clusters is None:
            raise Exception("Parameter num_cluster is None")

        return self.__cluster(input_events, image_frame)

    def cluster_kalman(self, data: numpy):
        return

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def spectral_clustering(
        num_clusters: int,
        num_neighbors: int,
    ) -> SpectralClustering:
        return SpectralClustering(
            n_clusters=num_clusters,
            random_state=0,
            affinity="precomputed_nearest_neighbors",
            n_neighbors=num_neighbors,
            assign_labels="kmeans",
            n_jobs=-1,
        )

    def nearest_neighbors(self, events: numpy.ndarray) -> NearestNeighbors:
        return kneighbors_graph(
            events,
            n_neighbors=self.num_neighbors,
        )

    def __cluster(
        self, input_events: numpy.array, image_frame: ImageFrame
    ) -> typing.Tuple[typing.List[numpy.ndarray], typing.Set[Detection]]:
        input_image: numpy = image_frame.pixels
        image_height, image_width = input_image.shape[0], input_image.shape[1]

        if input_events.shape[0] == 0:
            print("no events")
            return [], set()

        adjacency_matrix = self.nearest_neighbors(input_events)

        spectral_labels: numpy = GSCEventMOD.spectral_clustering(
            self.num_clusters, self.num_neighbors
        ).fit_predict(adjacency_matrix)

        spectral_labels = numpy.expand_dims(spectral_labels, axis=1)

        output_labels: numpy.array = ClusterUtils.convert_spectral_to_image(
            input_events, spectral_labels, image_height, image_width
        )

        return self.__retrieve_bounding_boxes(output_labels, image_frame)

    def calculate_silhouette_score(
        self, data: numpy.ndarray, clustering: numpy.ndarray
    ) -> float:
        return silhouette_score(data, clustering)

    def __retrieve_bounding_boxes(
        self, output_labels: numpy.ndarray, image_frame: ImageFrame
    ) -> typing.Tuple[typing.List[numpy.ndarray], typing.Set[Detection]]:
        detections: typing.Set[Detection] = set()
        bounding_boxes: typing.List[numpy.ndarray] = []

        for label in range(self.num_clusters):
            slice_x, slice_y = ndimage.find_objects(output_labels == label)[0]

            width: int = slice_x.stop - slice_x.start
            height: int = slice_y.stop - slice_y.start

            roi = image_frame.pixels[slice_x, slice_y]

            bounding_boxes.append(roi)
            detection: Detection = Detection(
                [slice_x.start, slice_y.start, width, height],
                timestamp=image_frame.timestamp,
                metadata={
                    "object_id": label,
                }
            )

            detections.add(detection)

        return bounding_boxes, detections

    def __get_bounding_boxes_corners(
        self, output_labels: numpy.ndarray
    ) -> numpy.ndarray:
        bounding_boxes: typing.List[typing.List] = []

        for label in range(self.num_clusters):
            slice_x, slice_y = ndimage.find_objects(output_labels == label)[0]
            bounding_boxes.append(
                [slice_x.start, slice_y.start, slice_x.stop, slice_y.stop]
            )

        return numpy.array(bounding_boxes)

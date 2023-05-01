from src.Models.ClusteringModel import ClusteringModel
from sklearn.cluster import SpectralClustering
import numpy
from stonesoup.types.sensordata import ImageFrame
import typing
from stonesoup.types.detection import Detection
from src.Utils.ClusterUtils import ClusterUtils


class GSCEventMOD(ClusteringModel):
    model_name = "GSC_EVENT_MOD"

    n_neighbors: int
    n_clusters: int

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def load_from_snapshot(self, session_to_restore_from: str) -> None:
        raise Exception("Not Implemented")

    def cluster(
        self, input_events: numpy.array, image_frame: ImageFrame
    ) -> typing.Tuple[typing.List[numpy.ndarray], typing.Set[Detection]]:
        return self.__cluster(input_events, image_frame)

    @staticmethod
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

    def __cluster(
        self, input_events: numpy.array, image_frame: ImageFrame
    ) -> typing.Tuple[typing.List[numpy.ndarray], typing.Set[Detection]]:
        """
        method for converting input_events and image_frame into bounding boxes.
        Parameters
        ----------
        input_events: numpy array of events in [x(1), y(1), ... , x(i), y(i)] format.
        image_frame: events in form of an image.

        Returns tuple of (list(bounding_box), set(Detection)); bounding_box: image of boxes.
        -------

        """
        input_image: numpy.ndarray = image_frame.pixels
        image_height, image_width = input_image.shape[0], input_image.shape[1]

        if input_events.shape[0] == 0:
            print("no events")
            return [], set()

        adjacency_matrix = ClusterUtils.get_nn_adjacency_matrix(input_events, self.n_neighbors)

        spectral_labels: numpy = GSCEventMOD.spectral_clustering(
            self.n_clusters,
            self.n_neighbors,
        ).fit_predict(adjacency_matrix)

        spectral_labels = numpy.expand_dims(spectral_labels, axis=1)

        output_labels: numpy.array = ClusterUtils.convert_spectral_to_image(
            input_events, spectral_labels, image_height, image_width
        )

        return ClusterUtils.retrieve_bounding_boxes(self.n_clusters, output_labels, image_frame)

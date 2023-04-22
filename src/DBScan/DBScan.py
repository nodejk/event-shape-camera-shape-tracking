import typing

import numpy
import pydantic

from src.Models.ClusteringModel import ClusteringModel
from sklearn.cluster import DBSCAN
from stonesoup.types.sensordata import ImageFrame
from stonesoup.types.detection import Detection
from src.Utils.ClusterUtils import ClusterUtils


class DBScanConfig(pydantic.BaseModel):
    eps: typing.Optional[float]
    min_samples: typing.Optional[int]
    metric: typing.Union[typing.Callable, str] = "euclidean"
    metric_params: typing.Optional[typing.Dict] = None
    algorithm: typing.Optional[
        typing.Literal[
            "auto",
            "ball_tree",
            "kd_tree",
            "brute",
        ]
    ] = "auto"
    leaf_size: int = 30
    p: typing.Optional[float]
    n_jobs: typing.Final[int] = -1


class DBScan(ClusteringModel):
    model_name = "DB_SCAN"

    _db_scan: typing.Optional[DBSCAN] = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        DBScan._db_scan = DBSCAN(**DBScanConfig(**kwargs).dict())

    def load_from_snapshot(self, session_to_restore_from: str) -> None:
        raise Exception("Not Implemented")

    def cluster(
        self, input_events: numpy.array, image_frame: ImageFrame
    ) -> typing.Tuple[typing.List[numpy.ndarray], typing.Set[Detection]]:
        return self.__cluster(input_events, image_frame)

    def __cluster(
        self, input_events: numpy.array, image_frame: ImageFrame
    ) -> typing.Tuple[typing.List[numpy.ndarray], typing.Set[Detection]]:
        input_image: numpy.ndarray = image_frame.pixels
        image_height, image_width = input_image.shape[0], input_image.shape[1]

        if input_events.shape[0] == 0:
            print("no events")
            return [], set()

        spectral_labels: numpy.ndarray = DBScan._db_scan.fit_predict(input_events)

        spectral_labels = numpy.expand_dims(spectral_labels, axis=1)

        output_labels: numpy.array = ClusterUtils.convert_spectral_to_image(
            input_events, spectral_labels, image_height, image_width
        )

        num_unique_values = len([i for i in numpy.unique(spectral_labels) if i != -1])

        return ClusterUtils.retrieve_bounding_boxes(num_unique_values, output_labels, image_frame)

from stonesoup.detector.base import DetectionReader
from stonesoup.buffered_generator import BufferedGenerator
from src.Models.ClusteringModel import ClusteringModel
from stonesoup.base import Property
from src.Models.Configuration import ModelParametersConfig
from stonesoup.reader.base import FrameReader
from stonesoup.types.sensordata import ImageFrame
import typing
import datetime
import numpy
from src.Utils.EventsUtils import EventsUtils
from stonesoup.types.detection import Detection


class DetectionStreamer(DetectionReader):
    model_configuration: ModelParametersConfig = Property(doc="Model Configuration")
    frame_reader: FrameReader = Property(doc="Frame Reader")
    model: ClusteringModel = Property(doc="Clustering Model")

    @BufferedGenerator.generator_method
    def detections_gen(self) -> typing.Tuple[datetime.datetime, typing.Set[Detection]]:  # type: ignore
        image_frame: ImageFrame

        spectral_labels: typing.List[numpy.ndarray]
        bounding_boxes: typing.Set[Detection]

        for image_frame in self.frame_reader:
            event: numpy.ndarray = EventsUtils.convert_image_to_event(image_frame.pixels)

            spectral_labels, bounding_boxes = self.model.cluster(event, image_frame)

            yield image_frame.timestamp, bounding_boxes

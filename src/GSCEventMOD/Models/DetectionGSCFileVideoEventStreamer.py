from stonesoup.detector.base import DetectionReader
from stonesoup.buffered_generator import BufferedGenerator
from src.GSCEventMOD.Models.GSCEventMOD import GSCEventMOD
from stonesoup.base import Property
from src.Models.Configuration import Configuration, ModelParametersConfig
from stonesoup.reader.base import FrameReader
from stonesoup.types.sensordata import ImageFrame
import typing
import datetime
import numpy
import matplotlib.pyplot as plt
import dv
from src.Utils.event import convert_image_to_event
from stonesoup.types.detection import Detection


class DetectionGSCFileVideoEventStreamer(DetectionReader):
    model_configuration: ModelParametersConfig = Property(doc="Model Configuration")
    frame_reader: FrameReader = Property(doc="Frame Reader")

    @BufferedGenerator.generator_method
    def detections_gen(self) -> typing.Tuple[datetime.datetime, typing.Set[Detection]]:
        model: GSCEventMOD = GSCEventMOD(**self.model_configuration.parameters)

        image_frame: ImageFrame

        spectral_labels: typing.List[numpy.ndarray]
        bounding_boxes: typing.Set[Detection]

        for image_frame in self.frame_reader:

            event: numpy.ndarray = convert_image_to_event(image_frame.pixels)

            spectral_labels, bounding_boxes = model.cluster(event, image_frame)
            # print(len(spectral_labels))
            #
            # fig, axes = plt.subplots(nrows=1, ncols=4)
            # fig.canvas.manager.full_screen_toggle()  # toggle fullscreen mode
            # axes[0].imshow(spectral_labels[0])
            # axes[1].imshow(spectral_labels[1])
            # # axes[2].imshow(spectral_labels[2])
            # axes[2].imshow(image_frame.pixels)
            #
            # plt.show()

            yield image_frame.timestamp, bounding_boxes

        # with dv.AedatFile(configuration.aedat_file_reader_config.path) as aedat_file:
        #     for event_frame in aedat_file["events"].numpy():
        #         event = DetectionGSCFileVideoEventStreamer.process_event(event_frame)
        #
        #         (
        #             timestamp,
        #             input_image,
        #         ) = DetectionGSCFileVideoEventStreamer.get_event_image(
        #             event_frame, height, width
        #         )
        #
        #         spectral_labels, bounding_boxes = model.cluster(event, input_image)
        #
        #         detection_set: typing.Set[Detection] = self.__detection_processor(
        #             bounding_boxes
        #         )
        #         # fig, axes = plt.subplots(nrows=1, ncols=3)
        #
        #         # axes[0].imshow(spectral_labels[0])
        #         # axes[1].imshow(spectral_labels[1])
        #         # axes[2].imshow(input_image)
        #         #
        #         # plt.show()
        #
        #         yield datetime.datetime.now(), detection_set

    @staticmethod
    def get_image_size(configuration: Configuration):
        height: int
        width: int

        with dv.AedatFile(configuration.aedat_file_reader_config.path) as aedat_file:
            height, width = aedat_file["events"].size

        return height, width

    @staticmethod
    def process_event(frame: numpy) -> numpy:
        event = []

        for _, packet in enumerate(frame):
            if packet[3] != 1:
                continue
            event.append([packet[1], packet[2]])

        event_numpy = numpy.array(event)

        return event_numpy

    def __detection_processor(
        self, bounding_boxes: typing.List[typing.List]
    ) -> typing.Set[Detection]:
        detection_set: typing.Set[Detection] = set()

        for box in bounding_boxes:
            detection: Detection = Detection(box, timestamp=datetime.datetime.now())

            detection_set.add(detection)

        return detection_set

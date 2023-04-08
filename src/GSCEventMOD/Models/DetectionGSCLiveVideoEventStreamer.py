from stonesoup.detector.base import DetectionReader
from stonesoup.buffered_generator import BufferedGenerator
from src.GSCEventMOD.Models.GSCEventMOD import GSCEventMOD
import dv
import numpy
import typing


class DetectionGSCLiveVideoEventStreamer(DetectionReader):
    address: str
    port: int
    model_configurations: typing.Dict[typing.Any, typing.Any]

    model: GSCEventMOD = None

    HEIGHT: int = 100
    WIDTH: int = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_model(self) -> GSCEventMOD:
        if DetectionGSCLiveVideoEventStreamer.model == None:
            DetectionGSCLiveVideoEventStreamer.model = GSCEventMOD(
                self.model_configurations
            )
        return DetectionGSCLiveVideoEventStreamer.model

    @BufferedGenerator.generator_method
    def detections_gen(self):
        with dv.NetworkNumpyEventPacketInput(
            address=self.address, port=self.port
        ) as stream:
            model: GSCEventMOD = DetectionGSCLiveVideoEventStreamer.model

            for event_frame in stream:
                event = DetectionGSCLiveVideoEventStreamer.process_event(event_frame)

                yield model.cluster(event)

    @staticmethod
    def process_event(frame) -> numpy:
        height: int = DetectionGSCLiveVideoEventStreamer.HEIGHT
        width: int = DetectionGSCLiveVideoEventStreamer.WIDTH

        event = numpy.full((height, width), 0).astype(numpy.uint8)

        for packet in frame:
            if packet[3] == 1:
                event[packet[2]][packet[1]] = 255

        return event

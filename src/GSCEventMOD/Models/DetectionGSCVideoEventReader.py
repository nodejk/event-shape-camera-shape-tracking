from stonesoup.detector.base import DetectionReader
from stonesoup.buffered_generator import BufferedGenerator
from src.GSCEventMOD.Models.GSCEventMOD import GSCEventMOD
import dv
import numpy
import typing
import pydantic


class DetectionGSCVideoEventReader(DetectionReader, pydantic.BaseSettings):
    address: str
    port: int
    model_configurations: typing.Dict[typing.Any, typing.Any]

    model: GSCEventMOD = None

    HEIGHT: int = 100
    WIDTH: int = 100

    def get_model(self) -> GSCEventMOD:
        if DetectionGSCVideoEventReader.model == None:
            DetectionGSCVideoEventReader.model = GSCEventMOD(self.model_configurations)
        return DetectionGSCVideoEventReader.model

    @BufferedGenerator.generator_method
    def detections_gen(self):
        with dv.NetworkNumpyEventPacketInput(
            address=self.address, port=self.port
        ) as stream:
            model: GSCEventMOD = DetectionGSCVideoEventReader.model

            for event_frame in stream:
                event = DetectionGSCVideoEventReader.process_event(event_frame)

                yield model.cluster(event)

    @staticmethod
    def process_event(frame) -> numpy:
        height: int = DetectionGSCVideoEventReader.HEIGHT
        width: int = DetectionGSCVideoEventReader.WIDTH

        event = numpy.full((height, width), 0).astype(numpy.uint8)

        for packet in frame:
            if packet[3] == 1:
                event[packet[2]][packet[1]] = 255

        return event

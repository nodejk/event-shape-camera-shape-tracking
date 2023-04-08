from stonesoup.detector.base import DetectionReader
from stonesoup.buffered_generator import BufferedGenerator
from src.GSCEventMOD.Models.GSCEventMOD import GSCEventMOD
import dv
import numpy
import typing

# 
class DetectionGSCLiveVideoEventStreamer(DetectionReader):
    address: str
    port: int
    model_configurations: typing.Dict[typing.Any, typing.Any]

    model: GSCEventMOD = None

    HEIGHT: int = 100
    WIDTH: int = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Initialize the Model as GSCEventMOD if it wasnt initialized before, using the configurations from config file
    def get_model(self) -> GSCEventMOD:
        if DetectionGSCLiveVideoEventStreamer.model == None:
            DetectionGSCLiveVideoEventStreamer.model = GSCEventMOD(
                self.model_configurations
            )
        return DetectionGSCLiveVideoEventStreamer.model

    # 
    @BufferedGenerator.generator_method
    def detections_gen(self):
        # Get the live video stream, using the defined address and port
        with dv.NetworkNumpyEventPacketInput(
            address=self.address, port=self.port
        ) as stream:
            model: GSCEventMOD = DetectionGSCLiveVideoEventStreamer.model

            # Process every frame in the stream
            for event_frame in stream:
                event = DetectionGSCLiveVideoEventStreamer.process_event(event_frame)
                # Call clustering function from GSCEventMOD for every frame given the events from the frame
                yield model.cluster(event)


    # Gets events from every frame, returns the collected events array
    @staticmethod
    def process_event(frame) -> numpy:
        height: int = DetectionGSCLiveVideoEventStreamer.HEIGHT
        width: int = DetectionGSCLiveVideoEventStreamer.WIDTH

        event = numpy.full((height, width), 0).astype(numpy.uint8)

        # Packet = [X-coordinate, Y-Coordinate, EventHappened]
        # Gets event coordinates if it happened per frame
        for packet in frame:
            if packet[3] == 1:
                event[packet[2]][packet[1]] = 255

        return event

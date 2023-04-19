import numpy
from stonesoup.reader.base import FrameReader
from stonesoup.types.sensordata import ImageFrame
from stonesoup.base import Property
from stonesoup.buffered_generator import BufferedGenerator
from src.Utils.event import convert_event_frame_to_image, convert_packets_to_events
import dv
from src.DataProcessors import DataProcessorSteps
from src.DataTransformers import DataTransformerSteps
from src.EventDataProcessors import EventDataProcessorSteps


class LiveVideoStreamFrameReader(FrameReader):
    address: str
    port: int

    height: int
    width: int

    data_processors_steps: DataProcessorSteps = Property(doc="DataProcessor Steps")
    event_data_processors_steps: EventDataProcessorSteps = Property(
        doc="Event Data Processors"
    )
    data_transformers_steps: DataTransformerSteps = Property(
        doc="DataTransformers Steps"
    )

    @property
    def frame(self):
        return self.current

    @BufferedGenerator.generator_method
    def frames_gen(self) -> ImageFrame:
        with dv.NetworkNumpyEventPacketInput(
            address=self.address, port=self.port
        ) as stream:
            input_events: numpy.ndarray = convert_packets_to_events(stream)

            processed_events: numpy.ndarray = self.event_data_processors_steps.run(
                input_events
            )

            (image, timestamp) = convert_event_frame_to_image(
                processed_events,
                height=self.height,
                width=self.width,
            )

            processed_image: numpy.ndarray = self.data_transformers_steps.run(image)
            processed_image = self.data_processors_steps.run(processed_image)

            yield ImageFrame(processed_image, timestamp)

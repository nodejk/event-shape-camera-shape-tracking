import numpy
from stonesoup.reader.base import FrameReader
from stonesoup.types.sensordata import ImageFrame
from stonesoup.base import Property
from stonesoup.buffered_generator import BufferedGenerator
from src.Utils.event import convert_event_frame_to_image, convert_packets_to_events
import dv
import typing
from src.DataProcessors import DataProcessorSteps
from src.DataTransformers import DataTransformerSteps
from src.EventDataProcessors import EventDataProcessorSteps


class AedatFileFrameReader(FrameReader):
    file_path: str = Property(doc="Path of the aedat file")

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
        height, width = AedatFileFrameReader.get_image_size(self.file_path)

        with dv.AedatFile(self.file_path) as aedat_file:
            for packet in aedat_file["events"].numpy():
                input_events: numpy.ndarray = convert_packets_to_events(packet)

                processed_events = self.event_data_processors_steps.run(input_events)

                (image, timestamp) = convert_event_frame_to_image(processed_events, height, width)

                processed_image: numpy.ndarray = self.data_transformers_steps.run(image)
                processed_image = self.data_processors_steps.run(processed_image)

                yield ImageFrame(processed_image, timestamp)

    @staticmethod
    def get_image_size(file_path: str) -> typing.Tuple[int, int]:
        height: int
        width: int

        with dv.AedatFile(file_path) as aedat_file:
            height, width = aedat_file["events"].size

        aedat_file.close()

        return height, width

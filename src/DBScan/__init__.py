import os

import numpy
from matplotlib import pyplot
import matplotlib
import pathlib


from src.Models.Configuration import Configuration
from src.DBScan.DBScan import DBScan
from src.DataProcessors import DataProcessorSteps
from src.EventDataProcessors import EventDataProcessorSteps
from src.DataTransformers import DataTransformerSteps
from src.Models.DetectionStreamer import DetectionStreamer
from stonesoup.reader.base import FrameReader
from src.Enums.EventInputSourceType import EventInputSourceType
from src.Models.FrameReaders.LiveVideoStreamFrameReader import (
    LiveVideoStreamFrameReader,
)
from src.KalmanFilter.Models.KalmanFilter import KalmanFilter
from src.Models.Draw import Draw
from src.Models.FrameReaders.AedatFileFrameReader import AedatFileFrameReader
from src.Utils.SessionUtils import SessionUtils
from src.Models.Visualizer import Visualizer

matplotlib.use("TkAgg")


class Pipeline:
    configuration: Configuration

    frame_reader: FrameReader
    detection_streamer: DetectionStreamer

    data_processors_steps: DataProcessorSteps
    event_data_processors_steps: EventDataProcessorSteps
    data_transformers_steps: DataTransformerSteps

    model: DBScan

    def __init__(self, configuration: Configuration):
        self.configuration = configuration

        self.data_processors_steps = DataProcessorSteps(configuration)
        self.event_data_processors_steps = EventDataProcessorSteps(configuration)
        self.data_transformers_steps = DataTransformerSteps(configuration)

        self.frame_reader = self.__get_frame_reader()

        self.model = self.__get_model()

        self.detection_streamer = self.__get_detection_streamer()

        if self.configuration.model_output.save:
            self.model_output_path = SessionUtils.create_new_session(
                self.get_model_absolute_path,
                configuration,
            )
            self.saved_output_counter = 0

        self.__init_pipeline()

    def __get_model(self) -> DBScan:
        return DBScan(
            model_name=self.configuration.model,
            **self.configuration.model_parameters.parameters,
        )

    def __get_frame_reader(self) -> FrameReader:
        match self.configuration.events_input.source_type:
            case EventInputSourceType.LIVE.value:
                return LiveVideoStreamFrameReader(
                    **self.configuration.events_input.parameters,
                    data_processors_steps=self.data_processors_steps,
                    event_data_processors_steps=self.data_transformers_steps,
                    data_transformers_steps=self.data_transformers_steps,
                )
            case EventInputSourceType.FILE.value:
                return AedatFileFrameReader(
                    **self.configuration.events_input.parameters,
                    data_processors_steps=self.data_processors_steps,
                    event_data_processors_steps=self.data_transformers_steps,
                    data_transformers_steps=self.data_transformers_steps,
                )
            case _:
                raise Exception(
                    "Provide either {} or {} source type but given {}.".format(
                        EventInputSourceType.LIVE.value,
                        EventInputSourceType.FILE.value,
                        self.configuration.events_input.source_type,
                    )
                )

    def __get_detection_streamer(self) -> DetectionStreamer:
        return DetectionStreamer(
            self.configuration.model_parameters,
            self.frame_reader,
            self.model,
        )

    def __init_pipeline(self) -> None:
        kalman_filter: KalmanFilter = KalmanFilter(self.detection_streamer)
        pyplot.subplot(111)

        for timestamp, tracks in kalman_filter.tracker:
            image = Draw.draw_tracks(self.frame_reader.frame.pixels, tracks)

            if self.configuration.model_output.save:
                image_path = os.path.join(self.model_output_path, self.saved_output_counter.__str__() + ".jpg")
                Draw.save_image(image_path, image)
                self.saved_output_counter += 1

            if self.configuration.model_output.display:
                Visualizer.visualize(numpy.array(image), "model_output")

    def __real_time(self) -> None:
        raise NotImplementedError

    @property
    def get_model_absolute_path(self) -> str:
        return pathlib.Path(__file__).absolute().parent.__str__()

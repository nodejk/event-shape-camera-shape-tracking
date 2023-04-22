import typing
import os
from matplotlib import pyplot
import matplotlib
import copy
from PIL import Image
import pathlib


from src.Models.Configuration import Configuration
from src.GSCEventMOD.GSCEventMOD import GSCEventMOD
from stonesoup.reader.base import FrameReader
from src.Enums.PipelineEnum import PipelineEnum
from src.Enums.EventInputSourceType import EventInputSourceType
from src.Models.FrameReaders.AedatFileFrameReader import AedatFileFrameReader
from src.Models.FrameReaders.LiveVideoStreamFrameReader import (
    LiveVideoStreamFrameReader,
)
from src.KalmanFilter.Models.KalmanFilter import KalmanFilter
from src.Models.DetectionStreamer import DetectionStreamer
from src.DataProcessors import DataProcessorSteps
from src.EventDataProcessors import EventDataProcessorSteps
from src.DataTransformers import DataTransformerSteps
from src.Models.Draw import Draw
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

    model: GSCEventMOD

    current_session_path: str
    model_output_path: str

    saved_output_counter: int

    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration

        self.data_processors_steps = DataProcessorSteps(configuration)
        self.event_data_processors_steps = EventDataProcessorSteps(configuration)
        self.data_transformers_steps = DataTransformerSteps(configuration)

        self.frame_reader = self.__get_frame_reader()

        self.model = self.__get_model()

        self.detection_streamer = self.__get_detection_streamer()

        self.track_mapping = {}

        if self.configuration.model_output.save:
            self.model_output_path = SessionUtils.create_new_session(
                self.get_model_absolute_path,
                configuration,
            )
            self.saved_output_counter = 0

        self.__init_pipeline()

    def __init_pipeline(self):
        match self.configuration.pipeline_type:
            case PipelineEnum.REAL_TIME.value:
                return self.__real_time()
            case PipelineEnum.STEP_PREDICTION.value:
                return self.__step_prediction()
            case PipelineEnum.FIND_OPTIMAL_PARAMETERS.value:
                return self.__find_optimal_parameters()
            case _:
                raise Exception("Pipeline Type not found")

    def __save_configuration(self) -> None:
        configuration_path: str = os.path.join(self.current_session_path, "config.json")

        with open(configuration_path, "w") as file_pointer:
            file_pointer.write(self.configuration.json())

    @property
    def get_model_absolute_path(self) -> str:
        return pathlib.Path(__file__).absolute().parent.__str__()

    def __find_optimal_parameters(self) -> None:
        return

    def __get_model(self) -> GSCEventMOD:
        return GSCEventMOD(
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

    def __step_prediction(self) -> None:
        kalman_filter: KalmanFilter = KalmanFilter(self.detection_streamer)
        pyplot.subplot(111)

        for timestamp, detec in kalman_filter.tracker:
            frame = self.frame_reader.frame
            pixels = copy.deepcopy(frame.pixels)
            image = Image.fromarray(pixels)

            image = Draw.draw_tracks(image, detec)

            if self.configuration.model_output.save:
                image_path = os.path.join(
                    self.model_output_path, self.saved_output_counter.__str__() + ".jpg"
                )

                image.save(image_path)

                self.saved_output_counter += 1

    def __real_time(self) -> None:
        # streamer: DetectionStreamer = self.__get_video_streamer()
        #
        # detector: KalmanFilter = KalmanFilter(streamer)
        # tracker = detector.tracker
        #
        # for timestamp, detections in tracker:
        #     print(detections)
        pass

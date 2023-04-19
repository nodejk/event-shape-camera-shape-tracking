import typing
import os
import hashlib
from datetime import datetime
from matplotlib import pyplot
import matplotlib
import copy
from PIL import Image, ImageDraw
import numpy
import pathlib


from src.Models.Configuration import Configuration
from src.GSCEventMOD.Models.GSCEventMOD import GSCEventMOD
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
from src.Utils.file import random_file_name_generator
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")


class Pipeline:
    configuration: Configuration

    frame_reader: FrameReader
    detection_streamer: DetectionStreamer

    data_processors_steps: DataProcessorSteps
    event_data_processors_steps: EventDataProcessorSteps
    data_transformers_steps: DataTransformerSteps

    model: GSCEventMOD

    session_parent_folder: typing.Final[str] = "Sessions"
    model_output_folder: typing.Final[str] = "model_output"

    current_session_path: str
    model_output_path: str

    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration

        self.data_processors_steps = DataProcessorSteps(configuration)
        self.event_data_processors_steps = EventDataProcessorSteps(configuration)
        self.data_transformers_steps = DataTransformerSteps(configuration)

        self.frame_reader = self.__get_frame_reader()

        self.model = self.__get_model()

        if self.configuration.model_output.save:
            self.__create_new_session()
            self.__save_configuration()

            print('sessionpath-->', self.current_session_path)

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

    def __create_new_session(self) -> None:
        folder_name: str = random_file_name_generator()

        session_path: str = os.path.join(
            self.get_session_parent_absolute_path, folder_name
        )

        if not os.path.isdir(session_path):
            os.mkdir(session_path)

            self.current_session_path = session_path
            self.model_output_path = os.path.join(self.current_session_path, self.model_output_folder)

            os.mkdir(self.model_output_path)
        else:
            raise Exception("Session {} already exists".format(session_path))

    def __save_configuration(self) -> None:
        configuration_path: str = os.path.join(self.current_session_path, "config.json")

        with open(configuration_path, "w") as file_pointer:
            file_pointer.write(self.configuration.json())

    @property
    def get_session_parent_absolute_path(self) -> str:
        return os.path.join(
            pathlib.Path(__file__).absolute().parent, self.session_parent_folder
        )

    def __find_optimal_parameters(self) -> None:
        return

    def __get_model(self) -> GSCEventMOD:
        return GSCEventMOD(
            model_name=self.configuration.model,
            **self.configuration.model_parameters.parameters,
        )

    def __get_frame_reader(self):
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
        )

    def __step_prediction(self) -> None:
        detection_reader: DetectionStreamer = self.__get_detection_streamer()

        kalman_filter: KalmanFilter = KalmanFilter(detection_reader)
        ax1 = pyplot.subplot(111)

        first = True

        im1: typing.Any

        for timestamp, detec in kalman_filter.tracker:
            frame = self.frame_reader.frame
            pixels = copy.deepcopy(frame.pixels)
            image = Image.fromarray(pixels)

            image = self.draw_detections(image, detection_reader.detections)

            if self.configuration.model_output.save:
                file_name: str = random_file_name_generator()
                image_path = os.path.join(self.model_output_path, file_name + '.jpg')

                image.save(image_path)

    def draw_detections(self, image, detections):
        draw = ImageDraw.Draw(image)

        for index, detection in enumerate(detections):
            y0, x0, w, h = numpy.array(detection.state_vector).reshape(4)

            x1, y1 = (x0 + h, y0 + w)

            box1 = tuple([(x0, y0), (x1, y1)])

            draw.rectangle(box1, outline="red", width=3)

        return image

    def __real_time(self) -> None:
        # streamer: DetectionStreamer = self.__get_video_streamer()
        #
        # detector: KalmanFilter = KalmanFilter(streamer)
        # tracker = detector.tracker
        #
        # for timestamp, detections in tracker:
        #     print(detections)
        pass

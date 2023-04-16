from src.Models.AedatFileFrameReader import AedatFileFrameReader
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
import importlib

from src.Models.Configuration import Configuration
from src.GSCEventMOD.Models.GSCEventMOD import GSCEventMOD
from stonesoup.reader.base import FrameReader
from src.Enums.PipelineEnum import PipelineEnum
from src.Models.Visualizer import Visualizer
from src.Models.VideoStreamer import VideoStreamer
from src.KalmanFilter.Models.KalmanFilter import KalmanFilter
from src.GSCEventMOD.Models.DetectionGSCLiveVideoEventStreamer import (
    DetectionGSCLiveVideoEventStreamer,
)
from src.GSCEventMOD.Models.DetectionGSCFileVideoEventStreamer import (
    DetectionGSCFileVideoEventStreamer,
)
from src.DataProcessors import DataProcessorSteps
from src.EventDataProcessors import EventDataProcessorSteps
from src.DataTransformers import DataTransformerSteps
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")


class Pipeline:
    configuration: Configuration
    frame_reader: FrameReader
    video_streamer: VideoStreamer

    data_processors_steps: DataProcessorSteps
    event_data_processors_steps: EventDataProcessorSteps
    data_transformers_steps: DataTransformerSteps

    model: GSCEventMOD

    sessions_parent_path: str = "Sessions"
    session_path: str = None

    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration

        self.data_processors_steps = DataProcessorSteps(configuration)
        self.event_data_processors_steps = EventDataProcessorSteps(configuration)
        self.data_transformers_steps = DataTransformerSteps(configuration)

        self.frame_reader = self.__get_aedat_file_reader(
            self.data_processors_steps,
            self.event_data_processors_steps,
            self.data_transformers_steps,
        )

        self.model = self.__get_model()

        # self.__create_new_session()

        # self.__save_configuration()

        self.__init_pipeline()

    def __init_pipeline(
        self,
    ):
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
        current_timestamp: str = datetime.now().isoformat()
        hash_digest: str = hashlib.sha1(str.encode(current_timestamp)).hexdigest()[0:10]

        session_path: str = os.path.join(
            self.get_session_parent_absolute_path, hash_digest
        )

        if os.path.isdir(session_path) != True:
            os.mkdir(session_path)
            self.session_path = session_path
        else:
            raise Exception("Session {} already exists".format(session_path))

    def __save_configuration(self) -> None:
        configuration_path: str = os.path.join(self.session_path, "config.json")

        with open(configuration_path, "w") as file_pointer:
            file_pointer.write(self.configuration.json())

    @property
    def get_session_parent_absolute_path(self) -> str:
        return os.path.join(
            pathlib.Path(__file__).absolute().parent, self.sessions_parent_path
        )

    def __find_optimal_parameters(self) -> None:
        return

    def __get_model(self) -> GSCEventMOD:
        return GSCEventMOD(
            model_name=self.configuration.model,
            **self.configuration.model_parameters.parameters,
        )

    def __get_aedat_file_reader(
        self,
        data_processors_steps: DataProcessorSteps,
        event_data_processors_steps: EventDataProcessorSteps,
        data_transformers_steps: DataTransformerSteps,
    ) -> FrameReader:
        return AedatFileFrameReader(
            file_path=self.configuration.aedat_file_reader_config.path,
            data_processors_steps=data_processors_steps,
            event_data_processors_steps=event_data_processors_steps,
            data_transformers_steps=data_transformers_steps,
        )

    def __get_video_streamer(self) -> DetectionGSCLiveVideoEventStreamer:
        return DetectionGSCLiveVideoEventStreamer(
            address=self.configuration.detection_gsc_event_reader_config.address,
            port=self.configuration.detection_gsc_event_reader_config.port,
            model_configurations=self.configuration.model_parameters,
        )

    def __get_file_streamer(self) -> DetectionGSCFileVideoEventStreamer:
        return DetectionGSCFileVideoEventStreamer(
            self.configuration.model_parameters,
            self.frame_reader,
        )

    def __step_prediction(self) -> None:
        detection_reader: DetectionGSCFileVideoEventStreamer = (
            self.__get_file_streamer()
        )

        kalman_filter: KalmanFilter = KalmanFilter(detection_reader)
        ax1 = pyplot.subplot(111)

        first = True

        im1: typing.Any

        for timestamp, detec in kalman_filter.tracker:
            frame = self.frame_reader.frame
            pixels = copy.deepcopy(frame.pixels)
            image = Image.fromarray(pixels)

            image = self.draw_detections(image, detection_reader.detections)

            if first:
                im1 = ax1.imshow(image)
                first = False
                plt.ion()
            else:
                im1.set_data(image)
                pyplot.pause(0.001)

    def draw_detections(self, image, detections):
        draw = ImageDraw.Draw(image)

        print('detections-->', len(detections))
        for index, detection in enumerate(detections):
            print(index)
            y0, x0, w, h = numpy.array(detection.state_vector).reshape(4)

            x1, y1 = (x0 + h, y0 + w)

            box1 = tuple([(x0, y0), (x1, y1)])

            draw.rectangle(box1, outline="red", width=1)
            # draw.text((x0, y1 + 2), '{}'.format(index), fill=(255))

        return image

    def __transform_output(
        self, output: numpy.array, input: numpy.array
    ) -> numpy.array:
        points = numpy.asarray(
            [
                input[:][0][numpy.where(output == 1, True, False)],
                input[:][1][numpy.where(output == 1, True, False)],
            ]
        )

        return points.astype(numpy.uint8)

    def __visualize_output(self, input: numpy.array, output: numpy.array) -> None:
        Visualizer.visualize(input, "input")
        Visualizer.visualize(output, "output")

    def __real_time(self) -> None:
        streamer: DetectionGSCLiveVideoEventStreamer = self.__get_video_streamer()

        detector: KalmanFilter = KalmanFilter(streamer)
        tracker = detector.tracker

        for timestamp, detections in tracker:
            print(detections)

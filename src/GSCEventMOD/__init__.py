from src.Models.Configuration import Configuration
from src.Models.BaseDataProcessor import BaseDataProcessor
from src.Models.BaseDataTransformer import BaseDataTransformer
from src.GSCEventMOD.Models.GSCEventMOD import GSCEventMOD
from src.Enums.PipelineEnum import PipelineEnum
from src.Models.AedatFileReader import AedatFileReader
from src.Models.VideoStreamer import VideoStreamer
from src.KalmanFilter.Models.KalmanFilter import KalmanFilter
from src.GSCEventMOD.Models.DetectionGSCLiveVideoEventStreamer import (
    DetectionGSCLiveVideoEventStreamer,
)
from src.GSCEventMOD.Models.DetectionGSCFileVideoEventStreamer import (
    DetectionGSCFileVideoEventStreamer,
)
import typing
import os
import hashlib
import dv
import json
from datetime import datetime
from src.Models.Visualizer import Visualizer
import numpy
import pathlib
import importlib


class Pipeline:
    configuration: Configuration
    # AEDAT is data format for Dynamic Visions camera footage
    file_reader: AedatFileReader
    video_streamer: VideoStreamer
    data_processors: typing.List[BaseDataProcessor]
    data_transformers: typing.List[BaseDataTransformer]
    model: GSCEventMOD

    sessions_parent_path: str = "Sessions"
    session_path: str = None

    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration

        self.data_processors = self.__get_data_processors()

        self.data_transformers = self.__get_data_transformers()

        self.model = self.__get_model()

        # self.__create_new_session()
        
        # self.__save_configuration()

        # Load the pipeline time predefined in the config file
        match configuration.pipeline_type:
            case PipelineEnum.REAL_TIME.value:
                return self.__real_time()
            case PipelineEnum.STEP_PREDICTION.value:
                return self.__step_prediction()
            case PipelineEnum.FIND_OPTIMAL_PARAMETERS.value:
                return self.__find_optimal_parameters()
            case _:
                raise Exception("Pipeline Type not found")

    # 
    def __create_new_session(self) -> None:
        # Create a hash using SHA1 from current timestamp (random hash pretty much)
        current_timestamp: str = datetime.now().isoformat()
        hash_digest: str = hashlib.sha1(str.encode(current_timestamp)).hexdigest()[0:10]

        # Combine sessions directory path with random hash
        session_path: str = os.path.join(
            self.get_session_parent_absolute_path, hash_digest
        )

        # If the path generated using the random hash is a non-existent directory path
        # create this directory path in session, e.g. f91c19f5f2
        if os.path.isdir(session_path) != True:
            os.mkdir(session_path)
            self.session_path = session_path
        else:
            raise Exception("Session {} already exists".format(session_path))

    # Saves the configuration file to the config.json in the main directory of the project
    def __save_configuration(self) -> None:
        configuration_path: str = os.path.join(self.session_path, "config.json")

        with open(configuration_path, "w") as file_pointer:
            file_pointer.write(self.configuration.json())

    # Get the directory path from where this file is stored + "Sessions" to generate Sessions directory path
    @property
    def get_session_parent_absolute_path(self) -> None:
        return os.path.join(
            pathlib.Path(__file__).absolute().parent, self.sessions_parent_path
        )

    def __find_optimal_parameters(self) -> None:
        return

    # Gets the data processor which is necessary to load training data for a certain model
    # This one contains a cropping and noise filtering step
    def __get_data_processors(self) -> typing.List[BaseDataProcessor]:
        # Initialize as BaseDataProcessor, used for SQL operations
        data_processors: typing.List[BaseDataProcessor] = []

        # For every predefined step in the config file
        for processor_config in self.configuration.data_processors.steps:
            # Import the actual data processor and return it
            processor: BaseDataProcessor = importlib.import_module(
                f"src.DataProcessors.{processor_config.name}"
            ).DataProcessor(
                name=processor_config.name,
                **processor_config.parameters,
            )

            data_processors.append(processor)

        return data_processors

    # Gets the data transformer which is necessary to load training data for a certain model
    # This one contains a normalization step
    def __get_data_transformers(self) -> typing.List[BaseDataTransformer]:
        
        data_transformers: typing.List[BaseDataTransformer] = []

        for transformer_config in self.configuration.data_transformers:
            transformer: BaseDataTransformer = importlib.import_module(
                f"src.DataTransformers.{transformer_config.name}"
            ).DataTransformer(
                name=transformer_config.name,
                **transformer_config.parameters,
            )

            data_transformers.append(transformer)

        return data_transformers

    # Load the GSCEventMOD model, used for clustering event data
    def __get_model(self) -> GSCEventMOD:
        return GSCEventMOD(
            model_name=self.configuration.model,
            **self.configuration.model_parameters.parameters,
        )

    # Get the AEDAT format file reader
    # AEDAT is the file format the Dynamic Vision camera stores event data in
    def __get_file_reader(self) -> None:
        return AedatFileReader(path=self.configuration.aedat_file_reader_config.path)

    # Use the data processor, probably previously loaded using __get_data_processors, to process the input training data
    # Currently uses 2 steps:  cropping and noise filtering
    def __get_processed_data(self, input: numpy.array) -> None:
        output: numpy.array = input

        for processor in self.data_processors:
            output = processor.process_data(output)

        return output
    
    # Use the data transfomer, probably previously loaded using __get_data_transformers, to transform the input training data
    # Currently uses normalization
    def __get_transformed_data(self, input: numpy.array) -> None:
        output: numpy.array = input

        for transformer in self.data_transformers:
            output = transformer.transform(output)

        return output
    
    # Get the video stream from the predefined addres and port using the predefined model configurations
    # Predefinitions are mostly in config.json
    def __get_video_streamer(self) -> DetectionGSCLiveVideoEventStreamer:
        return DetectionGSCLiveVideoEventStreamer(
            address=self.configuration.detection_gsc_event_reader_config.address,
            port=self.configuration.detection_gsc_event_reader_config.port,
            model_configurations=self.configuration.model_parameters,
        )

    # Get the streamer function for reading a event data video file
    def __get_file_streamer(self) -> DetectionGSCFileVideoEventStreamer:
        return DetectionGSCFileVideoEventStreamer()

    # Not finished yet
    # should use the Kalman filtering technique to predict the next video frame given the current (and previous) frames
    def __step_prediction(self) -> None:
        streamer: DetectionGSCFileVideoEventStreamer = self.__get_file_streamer()

        detector: KalmanFilter = KalmanFilter(streamer)
        tracker = detector.tracker

        for timestamp, detec in tracker:
            # print(detections)
            
            # detections = trac
            print(detec, streamer.detections)

            # frame = frame_reader.frame
            # pixels = copy(frame.pixels)

            # Plot output
        #     image = Image.fromarray(pixels)
        #     image = draw_detections(image, detections)
        #     image = draw_tracks(image, tracks)
        #     ax3.axes.xaxis.set_visible(False)
        #     ax3.axes.yaxis.set_visible(False)
        #     fig3.tight_layout()
        #     artist = ax3.imshow(image, animated=True)
        #     artists3.append([artist])
        # ani3 = animation.ArtistAnimation(fig3, artists3, interval=20, blit=True, repeat_delay=200)

    # 
    def __transform_output(
        self, output: numpy.array, input: numpy.array
    ) -> numpy.array:
        points = numpy.asarray(
            [
                # numpy.where(condition, [x, y, ]/) returns elements chosen from x or y depending on condition
                input[:][0][numpy.where(output == 1, True, False)],
                input[:][1][numpy.where(output == 1, True, False)],
            ]
        )

        return points.astype(numpy.uint8)

    def __get_prediction(self, input: numpy.array) -> None:
        processed_data = self.__get_processed_data(input)
        transformed_data = self.__get_transformed_data(processed_data)

        return self.model.cluster(transformed_data)

    def __visualize_output(self, input: numpy.array, output: numpy.array) -> None:
        Visualizer.visualize(input, "input")
        Visualizer.visualize(output, "output")

    def __real_time(self) -> None:
        streamer: DetectionGSCLiveVideoEventStreamer = self.__get_video_streamer()

        detector: KalmanFilter = KalmanFilter(streamer)
        tracker = detector.tracker

        for timestamp, detections in tracker:
            print(detections)

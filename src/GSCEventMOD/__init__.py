from src.Models.Configuration import Configuration
from src.Models.BaseDataProcessor import BaseDataProcessor
from src.Models.BaseDataTransformer import BaseDataTransformer
from src.GSCEventMOD.Models.GSCEventMOD import GSCEventMOD
from src.Enums.PipelineEnum import PipelineEnum
from src.Models.AedatFileReader import AedatFileReader
from src.Models.VideoStreamer import VideoStreamer
from src.Models.EnvrionmentProvider import EnvironmentProvider
import typing
import os
import hashlib
import json
from datetime import datetime
from src.Models.Visualizer import Visualizer
import numpy
import pathlib
import importlib


class Pipeline:
    configuration: Configuration
    file_reader: AedatFileReader
    video_streamer: VideoStreamer
    data_processors: typing.List[BaseDataProcessor]
    data_transformers: typing.List[BaseDataTransformer]
    model: GSCEventMOD

    sessions_parent_path: str = 'Sessions'
    session_path: str = None

    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration

        self.data_processors = self.__get_data_processors()

        self.data_transformers = self.__get_data_transformers()        

        self.model = self.__get_model()

        # self.__create_new_session()
        # self.__save_configuration()

        match configuration.pipeline_type:
            case PipelineEnum.REAL_TIME.value: return self.__real_time()
            case PipelineEnum.STEP_PREDICTION.value: return self.__step_prediction()
            case PipelineEnum.FIND_OPTIMAL_PARAMETERS.value: return self.__find_optimal_parameters()
            case _:
                raise Exception('Pipeline Type not found')

    def __create_new_session(self) -> None:
        current_timestamp: str = datetime.now().isoformat()
        hash_digest: str = hashlib.sha1(str.encode(current_timestamp)).hexdigest()[0:10]

        session_path: str = os.path.join(self.get_session_parent_absolute_path, hash_digest)

        if (os.path.isdir(session_path) != True):
                os.mkdir(session_path)
                self.session_path = session_path
        else:
            raise Exception('Session {} already exists'.format(session_path))
    
    def __save_configuration(self) -> None:
        configuration_path: str = os.path.join(self.session_path, 'config.json')

        with open(configuration_path, 'w') as file_pointer:
            file_pointer.write(self.configuration.json())
    
    @property
    def get_session_parent_absolute_path(self) -> None:
        return os.path.join(pathlib.Path(__file__).absolute().parent, self.sessions_parent_path)


    def __find_optimal_parameters(self) -> None:
        return

    def __get_data_processors(self) -> typing.List[BaseDataProcessor]:        
        data_processors: typing.List[BaseDataProcessor] = []

        for processor_config in self.configuration.data_processors.steps:
            processor: BaseDataProcessor = importlib.import_module(
                f'src.DataProcessors.{processor_config.name}').DataProcessor(
                name=processor_config.name,
                **processor_config.parameters,
            )
            
            data_processors.append(processor)
                
        return data_processors
    
    def __get_data_transformers(self) -> typing.List[BaseDataTransformer]:
        data_transformers: typing.List[BaseDataTransformer] = []

        for transformer_config in self.configuration.data_transformers:
            transformer: BaseDataTransformer = importlib.import_module(
                f'src.DataTransformers.{transformer_config.name}').DataTransformer(
                name=transformer_config.name,
                **transformer_config.parameters,
            )

            data_transformers.append(transformer)

        return data_transformers

    def __get_model(self) -> GSCEventMOD:
        return GSCEventMOD(
            model_name= self.configuration.model,
            **self.configuration.model_parameters.parameters
        )

    def __get_file_reader(self) -> None:
        return AedatFileReader(
            path=self.configuration.aedat_file_reader_config.path
        )
    
    def __get_processed_data(self, input: numpy.array) -> None:
        output: numpy.array = input

        for processor in self.data_processors:
            output = processor.process_data(output)
        
        return output
    
    def __get_transformed_data(self, input: numpy.array) -> None:
        output: numpy.array = input

        for transformer in self.data_transformers:
            output = transformer.transform(output)
        
        return output
    
    def __get_video_streamer(self) -> VideoStreamer:
        return VideoStreamer(**EnvironmentProvider.VideoStreamerParameters())

    def __step_prediction(self) -> None:
        self.file_reader = self.__get_file_reader()

        for frame in self.file_reader:
            print(frame.shape)
            output: numpy.array = self.__get_prediction(frame)
            vid_output: numpy.array = self.__transform_output(output, frame)

            print(vid_output.shape)
            if (self.configuration.visualize):
                self.__visualize_output(frame, output)
        pass

    def __transform_output(self, output: numpy.array, input: numpy.array) -> numpy.array:
        points = numpy.asarray([
            input[:][0][numpy.where(output == 1, True, False)],
            input[:][1][numpy.where(output == 1, True, False)],
            ])
    
        return points.astype(numpy.uint8)
    
    def __get_prediction(self, input: numpy.array) -> None:
        processed_data = self.__get_processed_data(input)
        transformed_data = self.__get_transformed_data(processed_data)

        return self.model.cluster(transformed_data)

    def __visualize_output(self, input: numpy.array, output: numpy.array) -> None:
        Visualizer.visualize(input, 'input')
        Visualizer.visualize(output, 'output')

    def __real_time(self) -> None:
        self.video_streamer = self.__get_video_streamer()

        for frame in self.video_streamer:
            self.__visualize_output(frame, self.__get_prediction(frame))

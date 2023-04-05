from stonesoup.detector.base import DetectionReader
from stonesoup.buffered_generator import BufferedGenerator
from stonesoup.reader.base import SensorDataReader
import pydantic
from src.GSCEventMOD.Models.GSCEventMOD import GSCEventMOD
from src.Models.Configuration import Configuration
import typing
from src.Models.Visualizer import Visualizer
import datetime
import matplotlib.pyplot as plt
import numpy
import dv
import sys
import json


class DetectionGSCFileVideoEventStreamer(DetectionReader):
    @staticmethod
    def get_model_configuration() -> Configuration:
        config_file: str = './config.json'
        
        configuration: Configuration
        
        with open(config_file) as file:
            json_config = json.loads(file.read())
            configuration = Configuration(**json_config)
        
        return configuration
        
    @BufferedGenerator.generator_method
    def detections_gen(self) -> dv.Frame:
        
        configuration: Configuration = DetectionGSCFileVideoEventStreamer.get_model_configuration()
        
        model: GSCEventMOD = GSCEventMOD(
            model_name=configuration.model,
            **configuration.model_parameters.parameters
        )
        
        height, width = DetectionGSCFileVideoEventStreamer.get_image_size(configuration)
        
        with dv.AedatFile(configuration.aedat_file_reader_config.path) as aedat_file:
            detections = set()
            
            for event_frame in aedat_file["events"].numpy():
                
                events: typing.List[numpy.array] = []
                
                num_grouped_events: int = configuration.model_parameters.num_grouped_events
                
                event = DetectionGSCFileVideoEventStreamer.process_event(event_frame)
                
                input_image = DetectionGSCFileVideoEventStreamer.get_event_image(event_frame, height, width)
                
                spectral_labels = model.cluster(event, input_image)
                
                # image = GSCEventMOD.convert_spectral_to_image(event, spectral_labels, height, width)
                fig, axes = plt.subplots(nrows=1, ncols=3)
                
                axes[0].imshow(spectral_labels[0])
                axes[1].imshow(spectral_labels[1])
                axes[2].imshow(input_image)
                # plt.imshow(image)
                # plt.imshow(input_image)
                plt.show()
                # Visualizer.visualize(image, "test")
                
                
                
                yield datetime.datetime.now(), model.cluster(event)
    
    @staticmethod
    def get_image_size(configuration: Configuration):
        height: int
        width: int        

        with dv.AedatFile(configuration.aedat_file_reader_config.path) as aedat_file:
            height, width = aedat_file["events"].size
        
        return height, width
    
    @staticmethod
    def get_event_image(event: numpy, height: int, width: int) -> numpy:
        image: numpy = numpy.full((height, width), 0).astype(numpy.uint8)
        
        for packet in event:
            if (packet[3] == 1):
                x = packet[1]
                y = packet[2]
                
                image[y][x] =  255
        
        print('image-->', image.shape)
        return image
    
    @staticmethod
    def process_event(frame: numpy) -> numpy:        
        event = []
        
        for index, packet in enumerate(frame):    
            
            if (packet[3] != 1):
                continue
                
            event.append([packet[1], packet[2]])
        
        event_numpy = numpy.array(event)
                
        return event_numpy

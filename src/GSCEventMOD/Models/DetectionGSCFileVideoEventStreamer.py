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
from stonesoup.types.detection import Detection


class DetectionGSCFileVideoEventStreamer(DetectionReader):
    # Returns the configuration from the configuration file config.json safely
    @staticmethod
    def get_model_configuration() -> Configuration:
        config_file: str = './config.json'
        
        configuration: Configuration
        
        # Safely open the config file and read from it, store as Configuration 
        # with open(X) checks automatically if X exists and only procedes if it does
        with open(config_file) as file:
            json_config = json.loads(file.read())
            configuration = Configuration(**json_config)
        
        return configuration
    
    # 
    @BufferedGenerator.generator_method
    def detections_gen(self) -> dv.Frame:
        
        # Load the configuration safely
        configuration: Configuration = DetectionGSCFileVideoEventStreamer.get_model_configuration()
        
        model: GSCEventMOD = GSCEventMOD(
            model_name=configuration.model,
            **configuration.model_parameters.parameters
        )
        
        # Use stored image width/height
        height, width = DetectionGSCFileVideoEventStreamer.get_image_size(configuration)
        
        # DV = Dynamic Vision Sensors library
        # AEDAT = Format data is recorded in, the "video"
        with dv.AedatFile(configuration.aedat_file_reader_config.path) as aedat_file:
            
            # For every frame in the stored aedat-file
            for event_frame in aedat_file["events"].numpy():
                
                
                # Get events from the frame
                event = DetectionGSCFileVideoEventStreamer.process_event(event_frame)
                
                # Load the current frame image
                input_image = DetectionGSCFileVideoEventStreamer.get_event_image(event_frame, height, width)
                
                spectral_labels, bounding_boxes = model.cluster(event, input_image)
                
                detection_set: typing.Set[Detection] = self.__detection_processor(bounding_boxes)
                # image = GSCEventMOD.convert_spectral_to_image(event, spectral_labels, height, width)
                fig, axes = plt.subplots(nrows=1, ncols=3)
                
                # Shows the spectral labels as x/y and the image as a 2D plot
                axes[0].imshow(spectral_labels[0])
                axes[1].imshow(spectral_labels[1])
                # axes[2].imshow(spectral_labels[2])
                # axes[3].imshow(spectral_labels[3])
                axes[2].imshow(input_image)
                # plt.imshow(image)
                # plt.imshow(input_image)
                plt.show()
                
                
                
                yield datetime.datetime.now(), detection_set
    
    # Load the width and height from a AEDAT file (the Dynamic vision camera file format)
    @staticmethod
    def get_image_size(configuration: Configuration):
        height: int
        width: int        

        # Safely loads the AEDAT file, gets width/height from the size of the events per frame
        with dv.AedatFile(configuration.aedat_file_reader_config.path) as aedat_file:
            height, width = aedat_file["events"].size
        
        return height, width
    
    # 
    @staticmethod
    def get_event_image(event: numpy, height: int, width: int) -> numpy:
        # Creates a full numpy array with height/width of the image as an image array, fille with 0's 
        image: numpy = numpy.full((height, width), 0).astype(numpy.uint8)
        
        # Packet = [X-coordinate, Y-Coordinate, EventHappened]
        # For every possible event, check if it happened, then set the responding pixel in the image array
        for packet in event:
            if (packet[3] == 1):
                x = packet[1]
                y = packet[2]
                
                image[y][x] =  255
        
        return image
    
    # Gets all the events from a frame
    @staticmethod
    def process_event(frame: numpy) -> numpy:        
        event = []
        
        for _, packet in enumerate(frame):    
            
            if (packet[3] != 1):
                continue
            # Otherwise, append the event from the frame to the event array
            event.append([packet[1], packet[2]])
        
        # Make numpy-Array out of the events
        event_numpy = numpy.array(event)
                
        return event_numpy

    def __detection_processor(self, bounding_boxes: typing.List[typing.List]) -> typing.Set[Detection]:
        detection_set: typing.Set[Detection] = set()
        
        for box in bounding_boxes:
            detection: Detection = Detection(box, timestamp=datetime.datetime.now())
            
            detection_set.add(detection)
            
        return detection_set

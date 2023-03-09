from stonesoup.detector.base import DetectionReader
from stonesoup.buffered_generator import BufferedGenerator
from stonesoup.types.detection import Detection
from stonesoup.types.array import StateVector
from stonesoup.detector.tensorflow import TensorFlowBoxObjectDetector
import pydantic


class EventDetectionReader(DetectionReader, pydantic.BaseSettings):

    @BufferedGenerator.generator_method
    def detections_gen(self):

        
        yield 

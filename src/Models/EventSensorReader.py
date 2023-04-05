from stonesoup.reader.base import SensorDataReader
from stonesoup.buffered_generator import BufferedGenerator


class EventSensorReader(SensorDataReader):
    
    @BufferedGenerator.generator_method
    def groundtruth_paths_gen(self):
        pass
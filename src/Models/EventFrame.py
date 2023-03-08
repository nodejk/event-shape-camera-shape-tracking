import numpy
import datetime


class EventFrame:
    timestamp: int = None
    event: numpy.array

    def __init__(self, height: int, width: int) -> None:
        self.event = numpy.full((height, width), 0).astype(numpy.uint8)
        
    def reset_event(self) -> None:
        self.event.fill(0)
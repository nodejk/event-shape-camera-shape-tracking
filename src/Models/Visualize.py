import abc
from Models.EventCamera import EventCameraModel

class Visualize:

    def __init__(self, model: EventCameraModel) -> None:
        self.model: EventCameraModel = model
        pass

    @abc.abstractmethod
    def saveVisualization(self) -> None:
        pass

from abc import ABC, abstractmethod
from src.Models.EventCameraModel import EventCameraModel

class VisualizationAbstractModel():

    def __init__(self, model: EventCameraModel) -> None:
        self.model: EventCameraModel = model
        pass

    @abstractmethod
    def saveVisualization(self) -> None:
        pass

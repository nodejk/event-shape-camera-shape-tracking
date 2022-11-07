from src.EventCameraModels.KMeans import KMeans
from src.Models.ContextProviderModel import ContextProviderModel

class ContextProviderKMeansModel(ContextProviderModel):

    def __init__(self) -> None:
        super().__init__()

        self._model.fit(1, 2)
        
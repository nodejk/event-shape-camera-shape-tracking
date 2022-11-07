from src.Models.DataProcessorModel import DataProcessorModel

class Crop(DataProcessorModel):
    xLeft: int
    xRight: int
    yTop: int
    yBottom: int

    def __init__(self, configuration: dict) -> None:
        super().__init__(configuration)
    
    def processData(self, input):
        pass
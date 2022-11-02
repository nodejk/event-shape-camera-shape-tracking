from src.Models.DataProcessorModel import DataProcessorModel

class Crop(DataProcessorModel):
    xLeft: int
    xRight: int
    yTop: int
    yBottom: int

    def __init__(self, requiredParametersList: list) -> None:
        super().__init__(requiredParametersList)
    
    def processData(self, input):
        print("self.xLeft-->" + str(self.xLeft))
        print("self.xRight-->" + str(self.xRight))
        print("self.yTop-->" + str(self.yTop))
        print("self.yBottom-->" + str(self.yBottom))
        
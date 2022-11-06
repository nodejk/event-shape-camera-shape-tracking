from src.Models.DataProcessorModel import DataProcessorModel

class Rotation(DataProcessorModel):
    yRotation: int  # in degrees
    xRotation: int  # in degrees

    def __init__(self, configuration: dict) -> None:
        super().__init__(configuration)

    def processData(self, input):
        print('xRotation-->', str(self.xRotation))
        print('yRotation-->', str(self.yRotation))
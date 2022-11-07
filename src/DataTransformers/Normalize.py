from src.Models.DataTransformerModel import DataTransformerModel

class Normalize(DataTransformerModel):
    outputRangeMin: int
    outputRangeMax: int

    def __init__(self, configuration: dict) -> None:
        super().__init__(configuration)

    def transform(self) -> None:
       pass
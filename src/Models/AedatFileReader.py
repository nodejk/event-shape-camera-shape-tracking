import dv
import pydantic
from src.Models.Frame import Frame
import typing


class AedatFileReader(pydantic.BaseModel):
    path: str
    height: int = pydantic.Field(default=None)
    width: int = pydantic.Field(default=None)

    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)

        with dv.AedatFile(self.path) as aedat_file:
            self.height, self.width = aedat_file['events'].size
        
        aedat_file.close()
    
    def __iter__(self) -> dv.Frame:
        with dv.AedatFile(self.path) as aedat_file:
            for frame in aedat_file['frames']:
                yield frame
    
    def dimensions(self):
        return [self.height, self.width]

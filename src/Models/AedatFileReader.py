import dv
import pydantic
import typing
import numpy
import pandas as pd
from src.Models.EventFrame import EventFrame


class AedatFileReader(pydantic.BaseModel):
    path: str
    height: int = pydantic.Field(default=0)
    width: int = pydantic.Field(default=0)

    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)

        with dv.AedatFile(self.path) as aedat_file:
            self.height, self.width = aedat_file['events'].size
        
        aedat_file.close()

    
    def __iter__(self) -> dv.Frame:
        with dv.AedatFile(self.path) as aedat_file:

            print(aedat_file['events'].EventsLength())
            for frame in aedat_file['events']:
                # print("start", frame.from_fb())
                
                # print("ende", frame.timestamp_end_of_exposure)
                yield frame

    @property
    def __time_delay_between_each_packet(self):
        return 10_000
    
    def dimensions(self):
        return [self.height, self.width]

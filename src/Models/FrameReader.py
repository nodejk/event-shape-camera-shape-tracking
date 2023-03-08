from stonesoup.reader.base import FrameReader
from stonesoup.types.sensordata import ImageFrame
import pickle
import glob
import typing
import datetime


class FrameReader(FrameReader):
    parent_path: str
    paths: typing.List[str]

    def __init__(self, parent_path, *args, **kwargs):
        self.parent_path = parent_path
        self.paths = glob.glob(self.parent_path)
        super().__init__(*args, **kwargs)

    def frames_gen(self):
        for path in self.paths:
            with open(path, 'rb') as file_pointer:
                loaded_dictionary = pickle.load(file_pointer)
                image = loaded_dictionary['image']

            yield ImageFrame(image, datetime.datetime.now())

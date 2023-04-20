import typing
from stonesoup.types.track import Track
from PIL.Image import Image as PilImage
from PIL import ImageDraw
import numpy
from stonesoup.types.detection import Detection
from src.Models.DetectionMetaData import DetectionMetaData


class Draw:
    @staticmethod
    def draw_tracks(image: PilImage, tracks: typing.Set[Track]) -> PilImage:
        draw: ImageDraw = ImageDraw.Draw(image)

        y0: float
        x0: float
        width: float
        height: float
        for _, track in enumerate(tracks):
            y0, x0, width, height = numpy.array([
                numpy.array(state.state_vector[[0, 2, 4, 5]]).reshape(4) for state in track.states]
            )[-1]

            x1, y1 = (x0 + height, y0 + width)

            box1: typing.Tuple = tuple([(x0, y0), (x1, y1)])

            draw.rectangle(box1, outline="red", width=3)

            detection_metadata: DetectionMetaData = DetectionMetaData(**track.metadata)

            draw.text((x0, y1 + 2), '{}'.format(detection_metadata.object_id), fill='red')

        return image

    @staticmethod
    def draw_detections(image: PilImage, detections: typing.Set[Detection]) -> PilImage:
        draw: ImageDraw = ImageDraw.Draw(image)

        x0: float
        y0: float
        width: float
        height: float

        for index, detection in enumerate(detections):
            y0, x0, width, height = numpy.array(detection.state_vector).reshape(4)

            x1, y1 = (x0 + height, y0 + width)

            box1: typing.Tuple = tuple([(x0, y0), (x1, y1)])

            draw.rectangle(box1, outline="red", width=3)

        return image

import typing
from stonesoup.types.track import Track
from PIL.Image import Image as PilImage
from PIL import ImageDraw
import cv2 as cv
import numpy
from stonesoup.types.detection import Detection


class Draw:
    @staticmethod
    def draw_tracks(image: numpy.ndarray, tracks: typing.Set[Track]) -> numpy.ndarray:
        y0: float
        x0: float
        width: float
        height: float

        for track in tracks:
            y0, x0, width, height = numpy.array(
                [numpy.array(state.state_vector[[0, 2, 4, 5]]).reshape(4) for state in track.states]
            )[-1]

            track_id: str = track.id.__str__().split("-")[0][:3]

            x1, y1 = int(x0 + height), int(y0 + width)
            x0, y0 = int(x0), int(y0)

            cv.rectangle(image, (x0, y0), (x1, y1), (255, 255, 255), 2)

            cv.putText(image, track_id, (x0, y1 + 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)

        return image

    @staticmethod
    def save_image(save_path: str, image: numpy.ndarray) -> None:
        cv.imwrite(save_path, image)

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

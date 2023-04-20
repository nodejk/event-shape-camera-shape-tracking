import typing
import datetime
import numpy
from stonesoup.types.detection import Detection


class EventsUtils:
    @staticmethod
    def convert_image_to_event(image: numpy.ndarray) -> numpy.ndarray:
        if image.ndim != 2:
            raise ValueError("Expected image of 2 dimensions, got {}".format(image.ndim))

        event = []

        for iy, ix in numpy.ndindex(image.shape):   # type: ignore
            if image[iy, ix] != 0:
                event.append([iy, ix])

        event_numpy: numpy.ndarray = numpy.array(event)

        return event_numpy

    @staticmethod
    def convert_event_frame_to_image(
        event_frame: numpy.ndarray, height: int, width: int
    ) -> typing.Tuple[numpy.ndarray, datetime.datetime]:

        image: numpy.ndarray = numpy.full((height, width), 0).astype(numpy.uint8)
        timestamp: datetime.datetime = datetime.datetime.now()

        set_timestamp: bool = False

        for event in event_frame:
            if not set_timestamp:
                timestamp = datetime.datetime.fromtimestamp(event[2] / 1_000)
                set_timestamp = True

            if int(event[3]) == 1:
                x = int(event[0])
                y = int(event[1])

                image[y][x] = 255

        return image, timestamp

    @staticmethod
    def convert_packets_to_events(
        input_packets: numpy.ndarray,
    ) -> numpy.ndarray:
        events: typing.List[typing.List] = []

        for packet in input_packets:
            events.append(
                [
                    packet[1],
                    packet[2],
                    packet[0] / 1_000,
                    packet[3],
                ]
            )

        return numpy.array(events)

    @staticmethod
    def convert_bounding_boxes_to_detections(
        bounding_boxes: typing.List[typing.List],
    ) -> typing.Set[Detection]:
        detection_set: typing.Set[Detection] = set()

        for box in bounding_boxes:
            detection: Detection = Detection(box, timestamp=datetime.datetime.now())

            detection_set.add(detection)

        return detection_set

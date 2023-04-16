import datetime
import numpy
import functools


def current_time_stamp(name: str) -> str:
    date_time_obj = datetime.datetime.now()
    return (
        date_time_obj.year.__str__()
        + "_"
        + date_time_obj.month.__str__()
        + "_"
        + date_time_obj.day.__str__()
        + "_"
        + date_time_obj.hour.__str__()
        + "_"
        + date_time_obj.minute.__str__()
        + "_"
        + date_time_obj.second.__str__()
        + "_"
        + name
    )


@functools.lru_cache(10)
def convert_seconds_to_timestamp(
    timestamp_second: numpy.int64,
) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(timestamp_second)


@functools.lru_cache(10)
def convert_micro_seconds_to_milli_seconds(
    timestamp_micro_second: numpy.int64,
) -> int:
    return timestamp_micro_second / 1_000


@functools.lru_cache(10)
def convert_milli_second_to_seconds(
    timestamp_milli_second: numpy.int64,
) -> int:
    return timestamp_milli_second / 1_000

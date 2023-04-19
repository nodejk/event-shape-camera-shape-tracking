from enum import Enum


class EventInputSourceType(str, Enum):
    LIVE: str = "live"
    FILE: str = "file"

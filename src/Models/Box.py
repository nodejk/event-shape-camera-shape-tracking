import pydantic

class Box(pydantic.BaseSettings):
    x: int
    y: int
    width: int
    height: int

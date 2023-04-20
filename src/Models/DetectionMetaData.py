import pydantic


class DetectionMetaData(pydantic.BaseModel):
    object_id: int

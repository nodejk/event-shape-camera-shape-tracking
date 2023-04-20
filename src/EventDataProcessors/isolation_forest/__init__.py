import copy
import typing

from src.Models.BaseDataProcessor import BaseDataProcessor
import numpy
from sklearn.ensemble import IsolationForest


class DataProcessor(BaseDataProcessor):
    random_state: int
    contamination: float

    _isolation_forest: typing.Optional[IsolationForest] = None

    def __init__(self, **kwargs) -> None:
        parent_attributes: typing.List[str] = [
            attr for attr in super().__annotations__.keys()
        ]

        super().__init__(**kwargs)

        DataProcessor._isolation_forest = IsolationForest(
            **{key: kwargs[key] for key in kwargs if key not in parent_attributes}
        )

    def process_data(self, input_events: numpy.ndarray):

        if self._isolation_forest is None:
            raise Exception("Isolation forest not initialized.")

        event_fires: numpy.ndarray = copy.deepcopy(input_events[:, 3])

        input_events[:, 3] = 0

        self._isolation_forest.fit(input_events)
        unwanted_events = self._isolation_forest.predict(input_events)

        input_events[:, 3] = event_fires

        return input_events[numpy.where(unwanted_events == 1, True, False)]

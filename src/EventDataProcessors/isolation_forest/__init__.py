import copy

from src.Models.BaseDataProcessor import BaseDataProcessor
import numpy
from sklearn.ensemble import IsolationForest
from functools import lru_cache


class DataProcessor(BaseDataProcessor):
    random_state: int
    contamination: float

    @staticmethod
    @lru_cache(maxsize=None)
    def isolation_forest(
            random_state: int,
            contamination: float,
    ) -> IsolationForest:
        return IsolationForest(
            random_state=random_state,
            contamination=contamination,
            n_jobs=-1,
        )

    def process_data(self, input_events: numpy.ndarray):
        isolation_forest: IsolationForest = DataProcessor.isolation_forest(
            self.random_state,
            self.contamination,
        )

        event_fires: numpy.ndarray = copy.deepcopy(input_events[:, 3])

        input_events[:, 3] = 0

        isolation_forest.fit(input_events)
        unwanted_events = isolation_forest.predict(input_events)

        input_events[:, 3] = event_fires

        return input_events[numpy.where(unwanted_events == 1, True, False)]

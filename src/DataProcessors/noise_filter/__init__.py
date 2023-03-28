from src.Models.BaseDataProcessor import BaseDataProcessor
import numpy
from sklearn.ensemble import IsolationForest
import typing
import joblib
import pydantic


class DataProcessor(BaseDataProcessor):
    load_model: bool
    model_path: str
    random_state: int
    n_jobs: int
    contamination: int
    isoloation_forest: IsolationForest = None

    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)

        if self.load_model:
            self.isoloation_forest = joblib.load(self.model_path)
        else:
            self.isoloation_forest = IsolationForest(
                random_state=self.random_state,
                n_jobs=self.n_jobs,
                contamination=self.contamination,
            )

    def process_data(self, input: numpy.array):
        if self.load_model:
            unwanted_input: numpy.array = self.isoloation_forest.predict(input)

            return input[numpy.where(unwanted_input == 1, True, False)]
        else:
            clean_input: IsolationForest = self.isoloation_forest.fit(input)
            unwanted_input: numpy.array = clean_input.predict(input)

            return input[numpy.where(unwanted_input == 1, True, False)]

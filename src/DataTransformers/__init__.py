import typing

import numpy

from src.Models.Configuration import Configuration
from src.Models.BaseDataTransformer import BaseDataTransformer
import importlib
import copy


class DataTransformerSteps:
    _data_transformers: typing.List[BaseDataTransformer]

    def __init__(self, configuration: Configuration):
        self._data_transformers = DataTransformerSteps.build(configuration)

    @staticmethod
    def build(configuration: Configuration) -> typing.List[BaseDataTransformer]:
        data_transformers: typing.List[BaseDataTransformer] = []

        for transformer_config in configuration.data_transformers.steps:
            transformer: BaseDataTransformer = importlib.import_module(
                f"src.DataTransformers.{transformer_config.name}"
            ).DataTransformer(
                name=transformer_config.name,
                **transformer_config.parameters,
            )

            data_transformers.append(transformer)

        return data_transformers

    def run(self, input_data: numpy.ndarray) -> numpy.ndarray:
        output: numpy.ndarray = copy.deepcopy(input_data)

        processor: BaseDataTransformer
        for processor in self._data_transformers:
            output = processor.transform(output)

        return output

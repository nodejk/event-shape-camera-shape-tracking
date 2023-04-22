import typing

import numpy
import copy

from src.Models.Configuration import Configuration
from src.Models.BaseDataProcessor import BaseDataProcessor
import importlib


class DataProcessorSteps:
    _data_processors: typing.List[BaseDataProcessor]

    def __init__(self, configuration: Configuration):
        self._data_processors = DataProcessorSteps.build(configuration)

    @staticmethod
    def build(configuration: Configuration) -> typing.List[BaseDataProcessor]:
        data_processors: typing.List[BaseDataProcessor] = []

        for processor_config in configuration.data_processors.steps:
            processor: BaseDataProcessor = importlib.import_module(
                f"src.DataProcessors.{processor_config.name}"
            ).DataProcessor(
                name=processor_config.name,
                **processor_config.parameters,
            )
            data_processors.append(processor)

        return data_processors

    def run(self, input_data: numpy.ndarray) -> numpy.ndarray:
        output: numpy.ndarray = copy.deepcopy(input_data)

        processor: BaseDataProcessor
        for processor in self._data_processors:
            output = processor.process_data(output)

        return output

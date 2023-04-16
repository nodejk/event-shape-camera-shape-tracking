import typing

import numpy
import copy

from src.Models.Configuration import Configuration
from src.Models.BaseDataProcessor import BaseDataProcessor
import importlib


class EventDataProcessorSteps:
    _event_data_processors: typing.List[BaseDataProcessor]

    def __init__(self, configuration: Configuration):
        self._event_data_processors = EventDataProcessorSteps.build(configuration)

    @staticmethod
    def build(configuration: Configuration) -> typing.List[BaseDataProcessor]:
        event_data_processors: typing.List[BaseDataProcessor] = []

        for processor_config in configuration.event_data_processors.steps:
            processor: BaseDataProcessor = importlib.import_module(
                f"src.EventDataProcessors.{processor_config.name}"
            ).DataProcessor(
                name=processor_config.name,
                **processor_config.parameters,
            )
            event_data_processors.append(processor)

        return event_data_processors

    def run(self, input_data: numpy.ndarray) -> numpy.ndarray:
        output: numpy.ndarray = copy.deepcopy(input_data)

        processor: BaseDataProcessor
        for processor in self._event_data_processors:
            output = processor.process_data(output)

        return output

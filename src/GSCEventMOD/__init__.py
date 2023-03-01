from src.Models.Configuration import Configuration
from src.Models.BaseDataProcessor import BaseDataProcessor
from src.Models.BaseDataTransformer import BaseDataTransformer
from src.GSCEventMOD.Models.GSCEventMOD import GSCEventMOD
from src.Enums.PipelineEnum import PipelineEnum
import typing
import importlib


class Pipeline:
    data_processors: typing.List[BaseDataProcessor] = []
    data_transformer: typing.List[BaseDataTransformer] = []
    model: GSCEventMOD

    def __init__(self, configuration: Configuration) -> None:
        
        print('Loading Data Processors...')

        for processor_config in configuration.data_processors.steps:
            processor: BaseDataProcessor = importlib.import_module(
                f'src.DataProcessors.{processor_config.name}').DataProcessor(
                name=processor_config.name,
                **processor_config.parameters,
            )
            
            self.data_processors.append(processor)
        
        print('Loaded Data Processors!')

        print('Loading Data Transformers...')

        for transformer_config in configuration.data_transformers:
            transformer: BaseDataTransformer = importlib.import_module(
                f'src.DataTransformers.{transformer_config.name}').DataTransformer(
                name=transformer_config.name,
                **transformer_config.parameters,
            )

            self.data_transformer.append(transformer)

        print('Loaded Data Transformers')

        print('Loading the model...')
        self.model = GSCEventMOD(model_name= configuration.model,
                                 **configuration.model_parameters.parameters)

        print('Loaded the model!')

        match configuration.pipeline_type:
            case PipelineEnum.REAL_TIME.value: return self.real_time()
            case PipelineEnum.STEP_PREDICTION.value: return self.step_prediction()
            case _:
                raise Exception('Pipeline Type not found')


    def reader(self) -> None:
        return


    def step_prediction(self, ) -> None:
        
        pass

    def real_time(self, ) -> None:
        pass



import typing
from src.Models.Configuration import Configuration
import importlib
from src.utils.string import pascalCase
from pydantic.tools import parse_obj_as
from datetime import datetime
import json
import os

class Session:
    configuration: Configuration
    
    def __init__(self, config_path: str) -> None:
        if (config_path is None):
            raise Exception('Configuration File Not Provided')
        
        with open(config_path) as file:
            print('Loading the configuration...')
            json_configuration: dict[typing.Any, typing.Any] = json.loads(file.read())

            self.configuration = Configuration(**json_configuration)

        importlib.import_module(f'src.{self.configuration.model}').Pipeline(self.configuration)

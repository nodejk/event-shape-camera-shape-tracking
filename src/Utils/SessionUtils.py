import typing
import os

from src.Utils.FileUtils import FileUtils
from src.Models.Configuration import Configuration


class SessionUtils:
    session_folder: typing.Final[str] = "Sessions"
    model_output_folder: typing.Final[str] = "model_output"

    @staticmethod
    def create_new_session(absolute_model_path: str, configuration: Configuration) -> str:
        folder_name: str = FileUtils.random_file_name_generator()

        session_path: str = os.path.join(
            SessionUtils.get_session_absolute_path(absolute_model_path),
            folder_name,
        )

        if not os.path.isdir(session_path):
            os.mkdir(session_path)

            model_output_path: str = os.path.join(session_path, SessionUtils.model_output_folder)

            os.mkdir(model_output_path)

            SessionUtils.save_model_configuration(session_path, configuration)

            return model_output_path
        else:
            raise Exception("Session {} already exists".format(session_path))

    @staticmethod
    def save_model_configuration(current_session_path: str, configuration: Configuration) -> None:
        configuration_path: str = os.path.join(current_session_path, "config.json")

        with open(configuration_path, "w") as file_pointer:
            file_pointer.write(configuration.json())

    @staticmethod
    def get_session_absolute_path(absolute_model_path: str) -> str:
        return os.path.join(
            absolute_model_path,
            SessionUtils.session_folder,
        )

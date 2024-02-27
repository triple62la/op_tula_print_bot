import json
import os.path
from typing_extensions import TypedDict

Config = TypedDict("Config", {"token": str, "primary_admin": str})


def load_config() -> Config:
    path_to_config = os.getcwd() + "/config.json"

    if not os.path.exists(path_to_config):
        raise Exception("Файл конфигурации не обнаружен")
    else:
        with open(path_to_config, "r") as file:
            data = file.read()
            return json.loads(data)


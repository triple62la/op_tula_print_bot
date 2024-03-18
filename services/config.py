import json
import os.path
from typing_extensions import TypedDict

Config = TypedDict("Config", {"token": str, "primary_chat_id": int, "admins_list": list[str]})


def load_config() -> tuple[str, int, list[str]]:
    path_to_config = os.getcwd() + "/config.json"

    if not os.path.exists(path_to_config):
        raise Exception("Файл конфигурации не обнаружен")
    else:
        with open(path_to_config, "r") as file:
            jsn = file.read()
            data: Config = json.loads(jsn)
            if data.get("token", None) is None:
                raise Exception("Не удалось найти токен в файле конфигурации")
            elif data.get("primary_chat_id", None) is None:
                raise Exception("Не удалось найти primary_chat_id в файле конфигурации")
            elif data.get("admins_list", None) is None or data.get("admins_list") == []:
                raise Exception("Не удалось найти primary_admins в файле конфигурации, либо список пуст")
            return data["token"], data["primary_chat_id"], data["admins_list"]


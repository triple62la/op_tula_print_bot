import telebot.types as bot_types
from telebot.util import quick_markup
import json


def create_main_keyboard(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
    exec_btn = {"callback_data": f"execute#{task_uuid}"}
    setup_btn = {"callback_data": f"setup#{task_uuid}"}
    del_btn = {"callback_data": f"delete#{task_uuid}"}
    main_keyboard = quick_markup({"Печать": exec_btn, "Параметры": setup_btn, "Удалить": del_btn})

    return main_keyboard


def create_finished_keyboard(task_uuid: str) -> bot_types.InlineKeyboardMarkup:

    del_btn = {"callback_data": f"delete#{task_uuid}"}
    keyboard = quick_markup({"Удалить": del_btn})

    return keyboard

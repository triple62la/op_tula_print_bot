import telebot.types as bot_types
from telebot.util import quick_markup
import json

from services.print_service import PrinterNamesEnum


def create_main_keyboard(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
    exec_btn = {"callback_data": f"execute##{task_uuid}"}
    setup_btn = {"callback_data": f"setup##{task_uuid}"}
    del_btn = {"callback_data": f"delete##{task_uuid}"}
    main_keyboard = quick_markup({"Печать": exec_btn, "Параметры": setup_btn, "Отмена": del_btn})

    return main_keyboard


def create_finished_keyboard(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
    del_btn = {"callback_data": f"delete##{task_uuid}"}
    keyboard = quick_markup({"Удалить": del_btn})

    return keyboard


def create_settings_keyboard(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
    printer_btn = {"callback_data": f"setup_printer##{task_uuid}"}
    copies_btn = {"callback_data": f"setup_copies##{task_uuid}"}
    pages_btn = {"callback_data": f"setup_pages##{task_uuid}"}
    orientation_btn = {"callback_data": f"setup_orientation##{task_uuid}"}
    go_back_btn = {"callback_data": f"go_back##{task_uuid}"}
    main_keyboard = quick_markup(
        {"Принтер": printer_btn, "Кол-во копий": copies_btn, "Страницы": pages_btn, "Ориентация": orientation_btn,
         "Назад": go_back_btn})

    return main_keyboard


def create_printers_keyboard(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
    keys = {printer.value: {"callback_data": f"set_printer#{printer.value}#{task_uuid}"} for printer in
            PrinterNamesEnum}
    return quick_markup(keys)


def create_cancel_setup_btn(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
    keys = {"Отмена": {"callback_data": f"cancel_setup##{task_uuid}"}}
    return quick_markup(keys)


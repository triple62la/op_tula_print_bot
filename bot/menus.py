import telebot.async_telebot
from services.database.db_service import db_get_task_by_id
from services.database.models import Tasks, TaskStatusEnum
from services.print_service import OrientationEnum, PrintSettings, PrinterNamesEnum
import telebot.types as bot_types
from telebot.util import quick_markup


def compile_primary_msg(printer_name, copies, pages, orientation: int, task_status) -> str:
    if task_status == TaskStatusEnum.WAITING:
        task_status = "Ожидает отправки на печать"
    elif task_status == TaskStatusEnum.PENDING:
        task_status = "Задание было отправлено на печать. Файл и данное сообщение автоматически удалится с сервера в " \
                      "течение 1мин. "
    match orientation:
        case OrientationEnum.DEFAULT:
            orientation = "как в документе"
        case OrientationEnum.PORTRAIT:
            orientation = "Портретная"
        case OrientationEnum.LANDSCAPE:
            orientation = "Альбомная"

    return f"""
    Будет произведена печать файла с текущими настройками печати\n
            Принтер: {printer_name}
            Кол-во копий: {copies}
            Номера страниц: {pages or 'Все'}
            Ориентация: {orientation}

            \n{task_status}
            """


class InlineKeyboards:

    @staticmethod
    def main_keyboard(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
        exec_btn = {"callback_data": f"execute##{task_uuid}"}
        setup_btn = {"callback_data": f"setup##{task_uuid}"}
        del_btn = {"callback_data": f"delete##{task_uuid}"}
        main_keyboard = quick_markup({"Печать": exec_btn, "Параметры": setup_btn, "Отмена": del_btn})

        return main_keyboard

    @staticmethod
    def finished_keyboard(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
        del_btn = {"callback_data": f"delete##{task_uuid}"}
        keyboard = quick_markup({"Удалить": del_btn})

        return keyboard

    @staticmethod
    def settings_keyboard(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
        printer_btn = {"callback_data": f"setup_printer##{task_uuid}"}
        copies_btn = {"callback_data": f"setup_copies##{task_uuid}"}
        pages_btn = {"callback_data": f"setup_pages##{task_uuid}"}
        orientation_btn = {"callback_data": f"setup_orientation##{task_uuid}"}
        go_back_btn = {"callback_data": f"go_back##{task_uuid}"}
        main_keyboard = quick_markup(
            {"Принтер": printer_btn, "Кол-во копий": copies_btn, "Страницы": pages_btn, "Ориентация": orientation_btn,
             "Назад": go_back_btn})

        return main_keyboard

    @staticmethod
    def printers_keyboard(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
        keys = {printer.value: {"callback_data": f"set_printer#{printer.value}#{task_uuid}"} for printer in
                PrinterNamesEnum}
        return quick_markup(keys)

    @staticmethod
    def cancel_setup_btn(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
        keys = {"Отмена": {"callback_data": f"cancel_setup##{task_uuid}"}}
        return quick_markup(keys)

    @staticmethod
    def orientation_keyboard(task_uuid: str) -> bot_types.InlineKeyboardMarkup:
        keys = {"Портретная": {"callback_data": f"set_orientation#{OrientationEnum.PORTRAIT}#{task_uuid}"},
                "Альбомная": {"callback_data": f"set_orientation#{OrientationEnum.LANDSCAPE}#{task_uuid}"},
                "Как в документе": {"callback_data": f"set_orientation#{OrientationEnum.DEFAULT}#{task_uuid}"}
                }
        return quick_markup(keys)

class BotMenus:
    def __init__(self, bot: telebot.async_telebot.AsyncTeleBot):
        self.bot = bot

    async def send_main_menu(self, uid) -> bot_types.Message:
        task: Tasks = await db_get_task_by_id(uid)
        text: str = compile_primary_msg(task.printer_name, task.copies, task.pages,
                                        task.orientation, task.status)
        return await self.bot.edit_message_text(text, task.chat_id, task.reply_id,
                                                reply_markup=InlineKeyboards.main_keyboard(uid))

    async def reply_with_main_menu(self, to_message: bot_types.Message, task_uid: str,
                                   print_settings: PrintSettings):
        text: str = compile_primary_msg(print_settings.printer_name, print_settings.copies, print_settings.pages,
                                        print_settings.orientation, TaskStatusEnum.WAITING)

        return await self.bot.reply_to(to_message, text, reply_markup=InlineKeyboards.main_keyboard(str(task_uid)))

    async def send_settings_menu(self, task):
        await self.bot.edit_message_text("Параметры печати", task.chat_id, task.reply_id,
                                         reply_markup=InlineKeyboards.settings_keyboard(task.uuid))

    async def send_cancelled_msg(self, task):
        await self.bot.edit_message_text("Задание было отменено. Файл удален с сервера", task.chat_id, task.reply_id)

    async def send_executed_msg(self, task):
        await self.bot.edit_message_text(
            "Задание было отправлено на печать. Файл и данное сообщение автоматически удалится с сервера в течение 5мин.",
            task.chat_id, task.reply_id)

    async def ask_pages(self, task):
        await self.bot.edit_message_text(
            "Отправьте в чат через запятую нужные страницы для печати", task.chat_id,
            task.reply_id, reply_markup=InlineKeyboards.cancel_setup_btn(task.uuid))

    async def ask_copies(self, task):
        await self.bot.edit_message_text("Отправьте в чат число необходимых копий документа", task.chat_id,
                                         task.reply_id, reply_markup=InlineKeyboards.cancel_setup_btn(task.uuid))

    async def ask_printers(self, task):
        await self.bot.edit_message_text("Выберите принтер для печати текущего задания:", task.chat_id, task.reply_id,
                                         reply_markup=InlineKeyboards.printers_keyboard(task.uuid))

    async def ask_orientation(self, task):
        msg = "Выберите ориентацию печати"
        await self.bot.edit_message_text(msg, task.chat_id, task.reply_id, reply_markup=InlineKeyboards.orientation_keyboard(task.uuid))

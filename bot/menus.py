import telebot.async_telebot
import telebot.types
from bot.inline_keyboards import create_main_keyboard
from services.database.db_service import db_get_task_by_id
from services.database.models import Tasks, TaskStatusEnum
from services.print_service import OrientationEnum, PrintSettings, PrinterNamesEnum


def compile_primary_msg(printer_name, copies, pages, orientation:int, task_status) -> str:
    if task_status == TaskStatusEnum.WAITING:
        task_status = "Ожидает отправки на печать"
    elif task_status == TaskStatusEnum.PENDING:
        task_status = "Задание было отправлено на печать. Файл и данное сообщение автоматически удалится с сервера в " \
                      "течение 5мин. "
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


class BotMenus:
    def __init__(self, bot: telebot.async_telebot.AsyncTeleBot):
        self.bot = bot

    async def send_main_menu(self, uid) -> telebot.types.Message:
        task: Tasks = await db_get_task_by_id(uid)
        text: str = compile_primary_msg(task.printer_name, task.copies, task.pages,
                                        task.orientation, task.status)
        return await self.bot.edit_message_text(text, task.chat_id, task.reply_id,
                                                reply_markup=create_main_keyboard(uid))

    async def reply_with_main_menu(self, to_message: telebot.types.Message, task_uid: str,
                                   print_settings: PrintSettings):
        text: str = compile_primary_msg(print_settings.printer_name, print_settings.copies, print_settings.pages,
                                        print_settings.orientation, TaskStatusEnum.WAITING)

        return await self.bot.reply_to(to_message, text, reply_markup=create_main_keyboard(str(task_uid)))

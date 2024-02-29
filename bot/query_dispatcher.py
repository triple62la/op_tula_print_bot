import telebot.async_telebot
import telebot.types as bot_types

from services.database.db_service import db_get_task_by_id
from services.print_service import PrintSettings, OrientationEnum


class CallbackQueryDispatcher:
    def __init__(self, bot: telebot.async_telebot.AsyncTeleBot) -> None:
        self.bot = bot

    def enable(self) -> None:
        self.bot.register_callback_query_handler(callback=self.dispatch_callback_query, func=lambda callback: callback)

    async def dispatch_callback_query(self, callback: bot_types.CallbackQuery) -> None:
        action, payload = callback.data.split("#")
        match action:
            case "execute":
                await Actions.exec_print(payload)


class Actions:

    @staticmethod
    async def exec_print(payload):
        task = await db_get_task_by_id(payload)
        pages = task.pages.split(", ")
        settings = PrintSettings(task.printer_name, task.copies, task.pages, task.orientation)


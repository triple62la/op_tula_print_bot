import telebot.async_telebot
import telebot.types as bot_types

from bot.inline_keyboards import create_finished_keyboard
from bot.message_handlers import compile_primary_msg
from services.database.db_service import db_get_task_by_id, db_remove_task_by_id
from services.database.models import TaskStatusEnum
from services.print_service import PrintSettings, OrientationEnum, exec_task


class CallbackQueryDispatcher:
    def __init__(self, bot: telebot.async_telebot.AsyncTeleBot) -> None:
        self.bot = bot
        self.actions = Actions(bot)

    def enable(self) -> None:
        self.bot.register_callback_query_handler(callback=self.dispatch_callback_query, func=lambda callback: callback)

    async def dispatch_callback_query(self, callback: bot_types.CallbackQuery) -> None:
        action, uid = callback.data.split("#")
        match action:
            case "execute":
                await self.actions.on_execute(uid)
            case "setup":
                pass
            case "delete":
                await self.actions.on_delete(uid)

class Actions:

    def __init__(self, bot: telebot.async_telebot.AsyncTeleBot):
        self.bot = bot

    async def on_execute(self, uid):
        task = await db_get_task_by_id(uid)
        pages = task.pages.split(", ")
        settings = PrintSettings(task.printer_name, task.copies, pages, task.orientation)
        await exec_task(settings, task.file_path)
        await self.bot.edit_message_text(compile_primary_msg(task.printer_name,
                                                             task.copies,
                                                             task.pages,
                                                             task.orientation,
                                                             task_status=TaskStatusEnum.PENDING),
                                         task.chat_id, task.reply_id
                                         )

        await db_remove_task_by_id(uid)
    async def on_delete(self, uid):
        task = await db_get_task_by_id(uid)

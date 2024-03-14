import asyncio
import telebot.async_telebot
import telebot.types as bot_types
from bot.menus import BotMenus
from bot.states import SettingsState
from services.database.db_service import db_get_task_by_id, db_remove_task_by_id, db_set_param_by_id
from services.database.models import TaskStatusEnum, Tasks
from services.file_service import delete_file
from services.print_service import PrintSettings, exec_task


class CallbackQueryDispatcher:
    def __init__(self, bot: telebot.async_telebot.AsyncTeleBot) -> None:
        self.bot = bot
        self.actions = Actions(bot)

    def enable(self) -> None:
        self.bot.register_callback_query_handler(callback=self.dispatch_main_query, func=lambda callback: callback)

    async def dispatch_main_query(self, callback: bot_types.CallbackQuery) -> None:

        action, payload, uid = callback.data.split("#")
        task: Tasks = await db_get_task_by_id(uid)
        match action:
            case "execute":
                await self.actions.on_execute(uid, task)
            case "setup":
                await self.actions.on_setup(task)
            case "cancel_setup":
                await self.actions.on_cancel_setup(task)
            case "delete":
                await self.actions.on_delete(uid, task)
            case "setup_printer":
                await self.actions.on_setup_printer(task)
            case "set_printer":
                await self.actions.on_set_printer(payload, uid)
            case "setup_copies":
                await self.actions.on_setup_copies(task)
            case "setup_pages":
                await self.actions.on_setup_pages(task)
            case "setup_orientation":
                await self.actions.on_setup_orientation(task)
            case "set_orientation":
                await self.actions.on_set_orientation(task, payload)
            case "go_back":
                await self.actions.on_go_back(uid)


class Actions:

    def __init__(self, bot: telebot.async_telebot.AsyncTeleBot):
        self.bot = bot
        self.menus = BotMenus(bot)

    async def on_execute(self, uid, task):

        pages = task.pages.split(",") if task.pages else []
        settings = PrintSettings(task.printer_name, task.copies, pages, task.orientation)
        await exec_task(settings, task.file_path)
        await db_set_param_by_id(uid, status=TaskStatusEnum.PENDING)
        await self.menus.send_executed_msg(task)
        await asyncio.sleep(300)
        await db_remove_task_by_id(uid)
        delete_file(task.file_path)
        await self.bot.delete_message(task.chat_id, task.message_id)
        await self.bot.delete_message(task.chat_id, task.reply_id)

    async def on_delete(self, uid, task):
        delete_file(task.file_path)
        await db_remove_task_by_id(uid)
        await self.menus.send_cancelled_msg(task)

    async def on_setup(self, task):
        await self.menus.send_settings_menu(task)

    async def on_setup_printer(self, task: Tasks):
        await self.menus.ask_printers(task)
        # await self.bot.set_state(task.user_id, SettingsState.printer, task.chat_id)

    async def on_set_printer(self, payload: str, uid: str):
        await db_set_param_by_id(uid, printer_name=payload)
        await self.menus.send_main_menu(uid)

    async def on_setup_copies(self, task: Tasks):
        await self.menus.ask_copies(task)
        await self.bot.set_state(task.user_id, SettingsState.copies, task.chat_id)
        async with self.bot.retrieve_data(task.user_id, task.chat_id) as data:
            data["curr_uid"] = task.uuid

    async def on_cancel_setup(self, task: Tasks):
        await self.bot.delete_state(task.user_id, task.message_id)
        await self.menus.send_main_menu(task.uuid)

    async def on_setup_pages(self, task):
        await self.menus.ask_pages(task)
        await self.bot.set_state(task.user_id, SettingsState.pages, task.chat_id)
        async with self.bot.retrieve_data(task.user_id, task.chat_id) as data:
            data["curr_uid"] = task.uuid

    async def on_setup_orientation(self, task):
        await self.menus.ask_orientation(task)

    async def on_set_orientation(self, task, payload):
        await db_set_param_by_id(task.uuid, orientation=int(payload))
        await self.menus.send_main_menu(task.uuid)

    async def on_go_back(self, uid):
        await self.menus.send_main_menu(uid)

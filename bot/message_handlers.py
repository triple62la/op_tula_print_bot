import os
import uuid
import telebot.async_telebot
import telebot.types as bot_types
from telebot import asyncio_filters

from bot.menus import BotMenus
from bot.states import SettingsState
from services.database.db_service import db_create_task, db_set_param_by_id, db_get_task_by_id
from services.database.models import Tasks
from services.file_service import write_file
from services.print_service import DefaultPrintSettings


def setup_handlers(bot: telebot.async_telebot.AsyncTeleBot) -> None:
    menus = BotMenus(bot)

    @bot.message_handler(commands=["start"], chat_types=["supergroup"])
    async def handle_start_cmd(message: bot_types.Message):
        await bot.send_message(message.chat.id,
                               "Для печати напишите личное сообщение боту или закиньте в лс файл в формате PDF")

    @bot.message_handler(commands=["start"], chat_types=["private"])
    async def handle_start_cmd(message: bot_types.Message):
        await bot.send_message(message.chat.id, "Для печати перетащите в этот чат файл в формате PDF")

    @bot.message_handler(chat_types=["private"], content_types=["document"])
    async def handle_file(message: bot_types.Message):
        file_name = message.document.file_name
        if file_name.endswith(".pdf"):
            task_id = uuid.uuid4()
            file = await bot.get_file(message.document.file_id)
            file_data = await bot.download_file(file.file_path)
            file_path = os.getcwd() + "/downloads/" + file.file_id + ".pdf"
            await write_file(file_path, file_data)
            print_settings = DefaultPrintSettings()
            reply_msg = await menus.reply_with_main_menu(message, str(task_id), print_settings)
            await db_create_task(uuid=str(task_id),
                                 user_id=message.from_user.id,
                                 chat_id=message.chat.id,
                                 message_id=message.message_id,
                                 reply_id=reply_msg.message_id,
                                 printer_name=print_settings.printer_name,
                                 copies=print_settings.copies,
                                 pages=print_settings.pages,
                                 orientation=print_settings.orientation,
                                 file_path=file_path
                                 )
        else:
            await bot.reply_to(message, "В печать подходят только файлы формата PDF")

    @bot.message_handler(state=SettingsState.copies, is_digit=True)
    async def set_copies(message: bot_types.Message):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            uid = data["curr_uid"]
        await db_set_param_by_id(uid, copies=int(message.text))
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.delete_state(message.from_user.id, message.chat.id)
        await menus.send_main_menu(uid)

    @bot.message_handler(state=SettingsState.copies, is_digit=False)
    async def copies_incorrect(message: bot_types.Message):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            uid = data["curr_uid"]
        task = await db_get_task_by_id(uid)
        await bot.edit_message_text("Некорректный ввод. Введите необходимое число копий документа")

    @bot.message_handler(state=SettingsState.pages)
    async def set_pages(message: bot_types.Message):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            uid = data["curr_uid"]

        await db_set_param_by_id(uid, pages=message.text.replace(" ", ""))
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.delete_state(message.from_user.id, message.chat.id)
        await menus.send_main_menu(uid)

    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    bot.add_custom_filter(asyncio_filters.IsDigitFilter())

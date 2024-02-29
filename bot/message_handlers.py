import os
import uuid
import telebot.async_telebot
import telebot.types as bot_types

from bot.inline_keyboards import create_main_keyboard
from services.database.db_service import db_create_task
from services.file_service import write_file
from services.print_service import DefaultPrintSettings


def setup_handlers(bot: telebot.async_telebot.AsyncTeleBot) -> None:
    # @bot.my_chat_member_handler()
    # async def handle_chat_add(updated: bot_types.ChatMemberUpdated):
    #     if updated.difference["status"][1] in ["administrator", 'member']:
    #         current_groups.append(updated.chat)
    #     elif updated.difference["status"][1] == "left":
    #         for index, chat in enumerate(current_groups):
    #             if updated.chat.id == chat.id:
    #                 current_groups.pop(index)
    #                 break
    #     print(current_groups)

    @bot.message_handler(commands=["start"], chat_types=["supergroup"])
    async def handle_start_cmd(message: bot_types.Message):
        print(message.chat.id)
        print(await bot.get_chat(message.chat.id))
        await bot.send_message(message.chat.id,
                               "Для печати напишите личное сообщение боту или закиньте в лс файл в формате PDF")

    @bot.message_handler(commands=["start"], chat_types=["private"])
    async def handle_start_cmd(message: bot_types.Message):
        print(message.chat.id)
        print(await bot.get_chat(message.chat.id))
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
            await db_create_task(uuid=str(task_id),
                                 user_id=message.from_user.id,
                                 chat_id=message.chat.id,
                                 printer_name=print_settings.printer_name,
                                 copies=print_settings.copies,
                                 pages=print_settings.pages,
                                 orientation=print_settings.orientation,
                                 file_path=file_path
                                 )
            await bot.reply_to(message,
                               f"Будет произведена печать файла с текущими настройками печати\n{print_settings}",
                               reply_markup=create_main_keyboard(str(task_id)))


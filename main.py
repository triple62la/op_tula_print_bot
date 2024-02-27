import asyncio
import uuid

import aiofiles
import os
from telebot.async_telebot import AsyncTeleBot
import telebot.types as bot_types
from services.config import load_config
from services.print_service import DefaultPrintSettings
from services.inline_keyboards import create_main_keyboard

config = load_config()  # Токен передается через файл config.json

bot = AsyncTeleBot(config["token"])

current_groups: list[bot_types.Chat] = []
user_files = {}


@bot.my_chat_member_handler()
async def handle_chat_add(updated: bot_types.ChatMemberUpdated):
    if updated.difference["status"][1] in ["administrator", 'member']:
        current_groups.append(updated.chat)
    elif updated.difference["status"][1] == "left":
        for index, chat in enumerate(current_groups):
            if updated.chat.id == chat.id:
                current_groups.pop(index)
                break
    print(current_groups)


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
        directory = os.getcwd()
        file_full_path = directory + "/downloads/" + file.file_id + ".pdf"
        if not os.path.exists(directory + "/downloads"):
            os.mkdir(directory + "/downloads")
        async with aiofiles.open(file_full_path, "wb") as empty_file:
            await empty_file.write(file_data)
        # await bot.send_message(message.chat.id, "Начата печать файла: " + file_full_path)

        # await bot.send_message(message.chat.id, "Завершено: " + (stdout + stderr).decode("utf-8"))
        print_settings  = DefaultPrintSettings()
        await bot.reply_to(message, f"Будет произведена печать файла с текущими настройками печати\n{print_settings}",
                           reply_markup=create_main_keyboard(str(task_id)))

@bot.callback_query_handler(func = lambda callback: callback)
async def handle_query_callback(callback:bot_types.CallbackQuery):
    print(callback.data)


if __name__ == '__main__':
    asyncio.run(bot.infinity_polling())

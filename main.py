import asyncio
import aiofiles
import os
from telebot.async_telebot import AsyncTeleBot
import telebot.types as bot_types
import json
from .services.config import load_config

config = load_config() #Токен передается через файл config.json


bot = AsyncTeleBot(config["token"])





@bot.message_handler(commands=["/start"], chat_types=["public"])
async def handle_start_cmd(message: bot_types.Message):
    await bot.send_message(message.chat.id, "Для начала печати закиньте в диалог с ботом файл в формате PDF")


@bot.message_handler(chat_types=["private"], content_types=["document"])
async def handle_file(message: bot_types.Message):
    file_name = message.document.file_name
    if file_name.endswith(".pdf"):
        file = await bot.get_file(message.document.file_id)
        file_data = await bot.download_file(file.file_path)
        directory = os.getcwd()
        file_full_path = directory + "/downloads/" + file.file_id + ".pdf"
        if not os.path.exists(directory + "/downloads"):
            os.mkdir(directory + "/downloads")
        async with aiofiles.open(file_full_path, "wb") as empty_file:
            await empty_file.write(file_data)
        await bot.send_message(message.chat.id, "Начата печать файла: " + file_full_path)
        cmd = rf'lp -d kyocera {file_full_path}'
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        await bot.send_message(message.chat.id, "Завершено: " + (stdout + stderr).decode("utf-8"))


if __name__ == '__main__':
    asyncio.run(bot.infinity_polling())

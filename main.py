import asyncio
import os

import telebot
from sqlalchemy.ext.asyncio import create_async_engine
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
from bot.query_dispatcher import CallbackQueryDispatcher
from telebot.async_telebot import AsyncTeleBot

from bot.message_handlers import setup_handlers
from services.config import load_config
from services.database.models import engine, Base

config = load_config()
# Загрузка данных из файла конфигурации

bot = AsyncTeleBot(config["token"])  # Токен передается через файл config.json
# инициализация бота

dispatcher: CallbackQueryDispatcher = CallbackQueryDispatcher(bot)
# инициализация диспатчера обработки query коллбеков
dispatcher.enable()
# включение диспатчера

setup_handlers(bot)
# Установка обработчиков сообщений


async def async_main() -> None:

    async with engine.begin() as conn:
        if os.name == "nt":
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await bot.infinity_polling()




if __name__ == '__main__':
    if os.name == "nt":
        print("Данная операционная система не поддерживается, приложение будет работать в демо режиме. "
              "Для полноценной работы функционала необходимо запускать приложение в среде Linux")
    asyncio.run(async_main())

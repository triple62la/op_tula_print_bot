import asyncio
import os
import telebot
import logging
from telebot.async_telebot import StateMemoryStorage
from bot.query_dispatcher import CallbackQueryDispatcher
from telebot.async_telebot import AsyncTeleBot
from bot.message_handlers import setup_handlers
from services.config import load_config
from services.database.models import engine, Base

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

config = load_config()
# Загрузка данных из файла конфигурации

# Now, you can pass storage to bot.
state_storage = StateMemoryStorage()  # you can initialize here another storage

bot = AsyncTeleBot(config["token"], state_storage=state_storage)  # Токен передается через файл config.json
# инициализация бота

# bot.add_custom_filter(StateFilter(bot))

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

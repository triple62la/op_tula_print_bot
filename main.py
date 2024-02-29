import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

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
        await conn.run_sync(Base.metadata.create_all)
    await bot.infinity_polling()




if __name__ == '__main__':
    asyncio.run(async_main())

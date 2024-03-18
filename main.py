import asyncio
import os
import sys
import telebot
import logging
from telebot.async_telebot import StateMemoryStorage
from bot.query_dispatcher import CallbackQueryDispatcher
from telebot.async_telebot import AsyncTeleBot
from bot.message_handlers import setup_handlers
from services.config import load_config
from services.database.models import engine, Base

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# Загрузка данных из файла конфигурации
# Конфиг содержит токен бота, id чата в котором бот будет проверять членство юзеров для авторизации и список юзеров
TOKEN, PRIMARY_CHAT_ID, ADMINS_LIST = load_config()


# это сторедж в котором хранятся стейты юзеров
state_storage = StateMemoryStorage()


# инициализация бота
# Токен передается через файл config.json
bot = AsyncTeleBot(TOKEN, state_storage=state_storage)


# инициализация диспатчера обработки query коллбеков
dispatcher: CallbackQueryDispatcher = CallbackQueryDispatcher(bot, PRIMARY_CHAT_ID)
# включение диспатчера
dispatcher.enable()


# Установка обработчиков сообщений
setup_handlers(bot, PRIMARY_CHAT_ID)





@bot.my_chat_member_handler(func=lambda updated: updated.chat.type != "private")
async def handle_bot_invite(updated: telebot.types.ChatMemberUpdated):
    # if updated.difference["status"][1] == "member" and updated.chat.id != PRIMARY_CHAT_ID:
    #     await bot.send_message(updated.chat.id, "Нельзя просто так взять и добавить этого бота в сторонние чаты")
    #     await bot.leave_chat(updated.chat.id)
    print(updated.chat.id)

async def async_main() -> None:
    async with engine.begin() as conn:
        if "--drop_tables" in sys.argv:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await bot.infinity_polling()


if __name__ == '__main__':
    if os.name == "nt":
        print("Данная операционная система не поддерживается, приложение будет работать в демо режиме. "
              "Для полноценной работы функционала необходимо запускать приложение в среде Linux")
    asyncio.run(async_main())

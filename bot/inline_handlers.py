
import telebot.async_telebot
import telebot.types
def setup_inline_handlers(bot: telebot.async_telebot.AsyncTeleBot):


    @bot.inline_handler
    async def test(tes:telebot.types.InlineQuery):
        print(tes.query)
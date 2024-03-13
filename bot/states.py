from telebot.asyncio_handler_backends import StatesGroup, State


# Just create different statesgroup
class SettingsState(StatesGroup):
    printer = State()  # statesgroup should contain states
    copies = State()
    pages = State()

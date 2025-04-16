from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData

class BuildNmap(StatesGroup):
    writing_ip = State()
    writing_params = State()
    scanning = State()

class BuildWhois(StatesGroup):
    writing_ip = State()
    scanning = State()

class BuildNikto(StatesGroup):
    writing_ip = State()
    scanning = State()

class BuildFuzz(StatesGroup):
    writing_ip = State()
    scanning = State()

class BuildChef(StatesGroup):
    writing_method = State()
    writing_cipher = State()
    working = State()
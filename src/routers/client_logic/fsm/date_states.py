from aiogram.fsm.state import StatesGroup, State


class NewDate(StatesGroup):
    date_admin = State()

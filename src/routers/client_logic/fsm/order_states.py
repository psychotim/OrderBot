from aiogram.fsm.state import StatesGroup, State


class NewOrder(StatesGroup):
    service = State()
    name = State()
    surname = State()
    date_client = State()
    phone = State()

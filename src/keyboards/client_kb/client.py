from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ClientCB(CallbackData, sep="__", prefix="my"):
    data_id: str
    action: str


def start_client_btn() -> types.ReplyKeyboardMarkup:
    kb_list = [
        [types.KeyboardButton(text='Услуги'),
         types.KeyboardButton(text='Доступные даты'),
         types.KeyboardButton(text='Помощь')],
        [types.KeyboardButton(text='Обо мне')]
    ]

    start_buttons = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb_list,
        input_field_placeholder="Выберите действие"
    )
    return start_buttons


def service_btn() -> types.ReplyKeyboardMarkup:
    kb_list = [
        [types.KeyboardButton(text='Ваксинг верхней губы')],
        [types.KeyboardButton(text='Коллагенирование бровей')],
        [types.KeyboardButton(text='Коррекция бровей')],
        [types.KeyboardButton(text='Окрашивания ресниц')],
        [types.KeyboardButton(text='Ламинирование ресниц')],
        [types.KeyboardButton(text='Коллагенирование ресниц')],
        [types.KeyboardButton(text='Коррекция и окрашивание бровей')],
        [types.KeyboardButton(text='Отмена')]
    ]

    service_buttons = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb_list,
        input_field_placeholder="Выберите действие"
    )
    return service_buttons


def price_btn() -> types.ReplyKeyboardMarkup:
    kb_list = [
        [types.KeyboardButton(text="Записаться")],
        [types.KeyboardButton(text="Вернуться")]
    ]

    price_buttons = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb_list,
        input_field_placeholder="Выберите действие"
    )
    return price_buttons


def get_admin_dates_ikb(data):
    dates_ik = InlineKeyboardBuilder()
    for i in data:
        dates_ik.row(types.InlineKeyboardButton(
            text=f"{i[1]}",
            callback_data=ClientCB(data_id=i[1], action="date_client").pack())
        )
    return dates_ik.as_markup()

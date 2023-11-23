from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class client_cb(CallbackData, sep="__", prefix="my"):
    data_id: str
    action: str


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

kblist = [
    [types.KeyboardButton(text="Записаться")],
    [types.KeyboardButton(text="Вернуться")]
]

price_buttons = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=kblist,
    input_field_placeholder="Выберите действие"
)


def get_admin_dates_ikb(data):
    dates_ik = InlineKeyboardBuilder()
    for i in map(lambda x: str(x[1]), data):
        dates_ik.row(types.InlineKeyboardButton(
            text=i,
            callback_data=client_cb(data_id=i, action="date_client").pack())
        )
    return dates_ik.as_markup()

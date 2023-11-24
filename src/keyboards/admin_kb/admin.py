from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class UserCB(CallbackData, sep="__", prefix="product"):
    data_id: str
    action: str


def start_admin_btn() -> types.ReplyKeyboardMarkup:
    kb_admin_main = [
        [types.KeyboardButton(text='Услуги'),
         types.KeyboardButton(text='Доступные даты'),
         types.KeyboardButton(text='Помощь')],
        [types.KeyboardButton(text='Админ-панель')]
    ]

    start_admin_buttons = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb_admin_main,
        input_field_placeholder='Выберите действие'
    )
    return start_admin_buttons


def admin_btn() -> types.ReplyKeyboardMarkup:
    kb_admin_panel = [
        [types.KeyboardButton(text='Добавить дату/время'),
         types.KeyboardButton(text='Доступные даты'),
         types.KeyboardButton(text='Все записи')],
        [types.KeyboardButton(text='Главное меню')]
    ]

    admin_buttons = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb_admin_panel,
        input_field_placeholder='Выберите действие'
    )
    return admin_buttons


def get_edit_ikb(user_id: int) -> types.InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.button(
        text='Удалить запись',
        callback_data=UserCB(data_id=f"{user_id}", action="delete_reg")
    )
    ikb.adjust(1)
    return ikb.as_markup()


def get_dates_ikb(data: list) -> types.InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    for i in data:
        ikb.button(
            text=f"{i[1]} ❌",
            callback_data=UserCB(data_id=str(i[0]), action="delete_date").pack()
        )
    ikb.adjust(1)
    return ikb.as_markup()

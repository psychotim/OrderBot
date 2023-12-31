from aiogram import types


def cancel_kb() -> types.ReplyKeyboardMarkup:
    btn_list = [
        [types.KeyboardButton(text="Отмена")]
    ]

    cancel_button = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=btn_list
    )

    return cancel_button

import os

from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db.queries.orm import AsyncORM as db
from aiogram import types, Router, F
from src.keyboards.admin import (
    start_admin_buttons,
    admin_buttons,
    user_cb,
    get_dates_ikb
)
from src.keyboards.basic import cancel_kb
from src.keyboards.client import start_buttons, price_buttons

basic_router = Router()


async def show_all_dates(message: types.Message, dates: list) -> None:
    if message.from_user.id == int(os.getenv('SUDO_ID')):
        await message.answer(
            'Вы перешли в раздел доступных дат',
            reply_markup=cancel_kb()
        )
        await message.answer(
            "Доступные даты:",
            reply_markup=get_dates_ikb(dates)
        )

    elif message.from_user.id != int(os.getenv('SUDO_ID')):
        if not dates:
            pass
        else:
            date_str = '\n'.join(date_tuple[1] for date_tuple in dates)
            await message.answer(
                f'Доступные даты: \n{date_str}',
                reply_markup=price_buttons
            )


@basic_router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    if message.from_user.id == int(os.getenv('SUDO_ID')):
        await message.answer(
            'Привет Босс, вы вошли в Админ-панель!',
            reply_markup=start_admin_buttons
        )
    else:
        await message.answer(
            f'{message.from_user.first_name}, привет!',
            reply_markup=start_buttons
        )


@basic_router.message(F.text == "Главное меню")
async def cmd_panel(message: types.Message) -> None:
    if message.from_user.id != int(os.getenv('SUDO_ID')):
        await message.answer(
            'Вы вернулись в главное меню',
            reply_markup=start_buttons
        )

    elif message.from_user.id == int(os.getenv('SUDO_ID')):
        await message.answer(
            'Вы вернулись в главное меню',
            reply_markup=admin_buttons
        )


@basic_router.message(F.text == "Помощь")
async def cmd_help(message: types.Message) -> None:
    await message.answer(
        'Возникли проблемы в работе бота?\n'
        'Напиши мне в --> @ocbunknown'
    )


@basic_router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    await message.answer(
        'Возникли проблемы в работе бота?\n'
        'Напиши мне в --> @ocbunknown'
    )


@basic_router.message(F.text == "Обо мне")
async def cmd_help(message: types.Message) -> None:

    about = ("Приветствую! Я Вера-мастер по коллагенированию/ламинированию ресниц; моделированию,"
             "коррекции и окрашиванию бровей. В 2019 году я окунулась в мир индустрии красоты и за эти годы приобрела "
             "достаточный опыт, для того, чтобы подарить своим клиентам роскошный взгляд, подчеркнуть естественную"
             " красоту и создать гармоничный образ. Я помогаю своим клиентам чувствовать себя уверенно "
             "и привлекательно в любых ситуациях.\n\n")

    instagram = ("· Instagram: @verasok_lashes_brows\n"
                 "· Telegram: @verasok83")
    text = f'{about}\n Мои соцсети:\n <b>{instagram}</b>'

    await message.answer(
        text,
        parse_mode='HTML',
        reply_markup=cancel_kb()
    )

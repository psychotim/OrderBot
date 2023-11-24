import os

from aiogram import types, Router, F

from src.keyboards.basic_kb import cancel_kb
from src.keyboards.client_kb.client import start_client_btn, price_btn
from src.keyboards.admin_kb.admin import (
    get_dates_ikb,
    start_admin_btn
)
from src.db.queries.orm import AsyncORM as db

basic_router = Router(name='basic')


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
                reply_markup=price_btn()
            )


@basic_router.message(F.text == "Доступные даты")
async def cmd_show_all_dates(message: types.Message) -> None:
    dates = await db.get_admin_date()
    sudo_id = int(os.getenv('SUDO_ID'))
    if not dates:
        await message.answer(
            'На данный момент нет доступных дат',
            reply_markup=cancel_kb()
        )
    else:
        await show_all_dates(message, dates)

    if message.from_user.id != sudo_id:
        if not dates:
            await message.answer(
                'На данный момент нет доступных дат',
                reply_markup=cancel_kb()
            )
        else:
            await message.answer(
                'Уважаемый клиент, если ни одна из предложенных дат вам не подходит,'
                ' мы предлагаем связаться с мастером и договориться о'
                ' более удобной для вас дате'
                ' и времени.\n'
                f'<i> Спасибо за понимание! </i>',
                parse_mode='HTML',
                reply_markup=price_btn()
            )


@basic_router.message(F.text == "Главное меню")
async def cmd_panel(message: types.Message) -> None:
    if message.from_user.id != int(os.getenv('SUDO_ID')):
        await message.answer(
            'Вы вернулись в главное меню',
            reply_markup=start_client_btn()
        )

    elif message.from_user.id == int(os.getenv('SUDO_ID')):
        await message.answer(
            'Вы вернулись в главное меню',
            reply_markup=start_admin_btn()
        )


@basic_router.message(F.text == "Вернуться")
async def cmd_get_all_clients(message: types.Message) -> None:
    if message.from_user.id == int(os.getenv('SUDO_ID')):
        await message.answer(
            "Вы вернулись в главное меню",
            reply_markup=start_admin_btn()
        )
    else:
        await message.answer(
            'Вы вернулись в главное меню',
            reply_markup=start_client_btn()
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

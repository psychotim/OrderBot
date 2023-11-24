import os

from aiogram.filters import CommandStart
from aiogram import types, Router
from src.keyboards.admin_kb.admin import start_admin_btn
from src.keyboards.client_kb.client import start_client_btn

start_router = Router(name='start')


@start_router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    if message.from_user.id == int(os.getenv('SUDO_ID')):
        await message.answer(
            'Привет Босс, вы вошли в Админ-панель!',
            reply_markup=start_admin_btn()
        )
    else:
        await message.answer(
            f'{message.from_user.first_name}, привет!',
            reply_markup=start_client_btn()
        )

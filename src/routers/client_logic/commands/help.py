from aiogram.filters import Command
from aiogram import types, F, Router

help_router = Router(name='help')


@help_router.message(F.text == "Помощь")
async def cmd_help(message: types.Message) -> None:
    await message.answer(
        'Возникли проблемы в работе бота?\n'
        'связь: \n @ocbunknown'
    )


@help_router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    await message.answer(
        'Возникли проблемы в работе бота?\n'
        'связь: \n @ocbunknown'
    )

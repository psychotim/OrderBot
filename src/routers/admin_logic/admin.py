import os

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from src.routers.client_logic.fsm.date_states import NewDate
from aiogram.types import CallbackQuery

from src.db.queries.orm import AsyncORM as db
from src.keyboards.basic_kb import cancel_kb
from src.keyboards.admin_kb.admin import (
    get_edit_ikb,
    admin_btn,
    UserCB
)

admin_router = Router(name='admin')


@admin_router.callback_query(UserCB.filter(F.action == "delete_date"))
async def cb_delete_date(query: CallbackQuery, callback_data: UserCB) -> None:
    date_to_delete = callback_data.data_id
    await db.delete_date(date_to_delete)
    await query.answer()
    await query.message.edit_text(f"Дата была удалена.")


@admin_router.callback_query(UserCB.filter(F.action == "delete_reg"))
async def cb_delete_user(query: CallbackQuery, callback_data: UserCB) -> None:
    if query.from_user.id == int(os.getenv('SUDO_ID')):
        date_to_delete = callback_data.data_id
        await db.delete_user(date_to_delete)
        await query.message.reply('Запись была удалена')


@admin_router.message(F.text == "Админ-панель")
async def cmd_admin(message: types.Message) -> None:
    if message.from_user.id == int(os.getenv('SUDO_ID')):
        await message.answer(
            'Админ-панель открыта',
            reply_markup=admin_btn()
        )
    else:
        await message.answer('Нет доступа.')


@admin_router.message(F.text == "Добавить дату/время")
async def add_date(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id == int(os.getenv('SUDO_ID')):
        await message.answer(
            'Напишите дату и время\nМожно также через строчку '
            'Например:\n01.01.2023\n02.02.2023\nи т.д...',
            reply_markup=cancel_kb()
        )
        await state.set_state(NewDate.date_admin)


@admin_router.message(NewDate.date_admin)
async def cmd_add_date(message: types.Message, state: FSMContext) -> None:
    if message.text == "Отмена":
        await message.answer(
            "Действие отменено. Возвращаюсь в меню",
            reply_markup=admin_btn()
        )
        await state.clear()
    else:
        await state.update_data(date_admin=message.text)
        await message.answer(
            'Дата и время были успешно записаны\nВведите ещё:'
            ' (Для отмены нажмите соответствующую кнопку)',
            reply_markup=cancel_kb()
        )
        await db.write_date(state)
        await state.set_state(NewDate.date_admin)


async def show_all_clients(message: types.Message, clients: list) -> None:
    for client in clients:
        client_info = f"ID заказа: {client[0]}\n" \
                      f"Тип услуги: {client[1]}\n" \
                      f"Имя: {client[2]} {client[3]}\n" \
                      f"Дата: {client[4]}\n" \
                      f"Номер: {client[5]}"

        await message.answer(
            client_info,
            reply_markup=get_edit_ikb(client[0])
        )


@admin_router.message(F.text == "Все записи")
async def cmd_get_all_clients(message: types.Message) -> None:
    if message.from_user.id == int(os.getenv('SUDO_ID')):
        clients = await db.get_all_clients()
        if not clients:
            await message.answer('На данный момент нету записей')

        await show_all_clients(message, clients)

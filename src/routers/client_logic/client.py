import os

import aiogram.exceptions
from aiogram import types, F, Router, Bot
import telegram.error
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.routers.client_logic.fsm.order_states import NewOrder
from src.keyboards.admin_kb.admin import admin_btn
from src.keyboards.basic_kb import cancel_kb

from src.keyboards.client_kb.client import (
    price_btn,
    get_admin_dates_ikb,
    service_btn,
    start_client_btn,
    ClientCB
)
from src.db.queries.orm import AsyncORM as db

client_router = Router(name='client_logic')


@client_router.message(F.text == "Отмена")
async def cmd_panel(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id == int(os.getenv('SUDO_ID')):
        await state.clear()
        await message.answer(
            'Вы вернулись обратно',
            reply_markup=admin_btn()
        )
    else:
        await state.clear()
        await message.answer(
            'Вы вернулись обратно',
            reply_markup=start_client_btn()
        )


@client_router.message(F.text == 'Услуги')
async def cmd_services(message: types.Message) -> None:
    price = '55 рублей'
    service = 'Коллагенирование ресниц'
    text = f'Услуга: {service}\n Цена услуги: <b>{price}</b>'
    await message.answer(text, parse_mode='HTML')

    price1 = '45 рублей'
    service1 = 'Ламинирование ресниц'
    text1 = f'Услуга: {service1}\n Цена услуги: <b>{price1}</b>'
    await message.answer(text1, parse_mode='HTML')

    price2 = '45 рублей'
    service2 = 'Коллагенирование бровей'
    text2 = f'Услуга: {service2}(Коррекция и окрашивание)\n Цена услуги: <b>{price2}</b>'
    await message.answer(text2, parse_mode='HTML')

    price3 = '20 рублей'
    service3 = 'Коррекция и окрашивание бровей'
    text3 = f'Услуга: {service3}\n Цена услуги: <b>{price3}</b>'
    await message.answer(text3, parse_mode='HTML')

    price4 = '15 рублей'
    service4 = 'Коррекция бровей'
    text4 = f'Услуга: {service4}\n Цена услуги: <b>{price4}</b>'
    await message.answer(text4, parse_mode='HTML')

    price5 = '10 рублей'
    service5 = 'Окрашивание ресниц'
    text5 = f'Услуга: {service5}\n Цена услуги: <b>{price5}</b>'
    await message.answer(text5, parse_mode='HTML')

    price6 = '8 рублей'
    service6 = 'Ваксинг верхней губы'
    text6 = f'Услуга: {service6}\n Цена услуги: <b>{price6}</b>'

    await message.answer(text6, parse_mode='HTML', reply_markup=price_btn())


@client_router.message(F.text == "Записаться")
async def cmd_add_service(message: types.Message, state: FSMContext) -> None:
    await state.set_state(NewOrder.service)
    await message.answer(
        'Выберите услугу:',
        reply_markup=service_btn()
    )


@client_router.message(NewOrder.service)
async def add_service(message: types.Message, state: FSMContext) -> None:
    await state.update_data(service=message.text)
    await state.set_state(NewOrder.name)
    await message.answer(
        'Напишите ваше имя:',
        reply_markup=cancel_kb()
    )


@client_router.message(NewOrder.name)
async def name_handler(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(NewOrder.surname)
    await message.answer(
        'Напишите вашу фамилию:',
        reply_markup=cancel_kb()
    )


@client_router.message(NewOrder.surname)
async def surname_handler(message: types.Message, state: FSMContext) -> None:
    date_admin = await db.get_admin_date()
    await state.update_data(surname=message.text)
    await state.set_state(NewOrder.date_client)

    if date_admin is None or len(date_admin) == 0:
        await message.answer('На данный момент нет доступных дат')
        await state.clear()
    else:
        await message.answer(
            'выберите дату:',
            reply_markup=get_admin_dates_ikb(date_admin)
        )


@client_router.callback_query(
    NewOrder.date_client,
    ClientCB.filter(F.action == "date_client")
)
async def date_select_handler(query: CallbackQuery, callback_data: ClientCB, state: FSMContext) -> None:
    date_client = callback_data.data_id
    await state.update_data(date_client=date_client)
    await query.answer()
    await state.set_state(NewOrder.phone)

    await query.message.answer(
        'Введите ваш номер телефона',
        reply_markup=cancel_kb()
    )


@client_router.message(NewOrder.phone)
async def add_service(message: types.Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(phone=message.text)

    if message.from_user.id != int(os.getenv('SUDO_ID')):
        await message.answer(
            'Вы записаны, как только мастер будет свободен, он с вами свяжется!\n'
            'Возникли вопросы?\n'
            ' Напишите мастеру --> @verasok83',
            reply_markup=start_client_btn()
        )
    else:
        await message.answer(
            'Вы на главном меню',
            reply_markup=admin_btn()
        )

    await db.add_item(state)
    await state.clear()

    try:
        await bot.send_message(
            chat_id=int(os.getenv('NOTICE_ID')),
            text='К вам новый клиент'
        )
    except (telegram.error.BadRequest, aiogram.exceptions.TelegramNotFound) as e:
        print('При отправке сообщения произошла ошибка:', e)

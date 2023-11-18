import os

import aiogram.exceptions
from aiogram import types, F, Router, Bot
import telegram.error
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from src.keyboards.admin import admin_buttons
from src.keyboards.basic import cancel_buttons
from .basic import show_all_dates

from src.keyboards.client import (
    price_buttons,
    get_admin_dates_ikb,
    service_buttons,
    start_buttons,
    client_cb
)
import src.utils.database as db


class NewOrder(StatesGroup):
    service = State()
    name = State()
    surname = State()
    date_client = State()
    phone = State()


class NewDate(StatesGroup):
    date_admin = State()


client_router = Router()


@client_router.message(F.text == "Доступные даты")
async def cmd_show_all_dates(message: types.Message):
    dates = await db.get_admin_date()
    sudo_id = int(os.getenv('SUDO_ID'))
    is_admin = await db.is_admin(message.from_user.id)
    if not dates:
        await message.answer('На данный момент нет доступных дат', reply_markup=cancel_buttons)
    else:
        await show_all_dates(message, dates)

    if message.from_user.id != sudo_id and not is_admin:
        if not dates:
            await message.answer('На данный момент нет доступных дат', reply_markup=cancel_buttons)
        else:
            await message.answer('Уважаемый клиент, если ни одна из предложенных дат вам не подходит,'
                                     ' мы предлагаем связаться с мастером и договориться о более удобной для вас дате'
                                     ' и времени.\n'
                                     f'<i> Спасибо за понимание! </i>',
                                     parse_mode='HTML', reply_markup=price_buttons)


@client_router.message(F.text == 'Услуги')
async def cmd_services(message: types.Message):
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
    await message.answer(text6, parse_mode='HTML', reply_markup=price_buttons)


@client_router.message(F.text == "Записаться")
async def cmd_add_service(message: types.Message, state: FSMContext):
    await state.set_state(NewOrder.service)
    await message.answer('Выберите услугу:', reply_markup=service_buttons)


@client_router.message(NewOrder.service)
async def add_service(message: types.Message, state: FSMContext):
    await state.update_data(service=message.text)
    await state.set_state(NewOrder.name)
    await message.answer('Напишите ваше имя:', reply_markup=cancel_buttons)


@client_router.message(NewOrder.name)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(NewOrder.surname)
    await message.answer('Напишите вашу фамилию:', reply_markup=cancel_buttons)


@client_router.message(NewOrder.surname)
async def surname_handler(message: types.Message, state: FSMContext):
    date_admin = await db.get_admin_date()
    await state.update_data(surname=message.text)
    await state.set_state(NewOrder.date_client)
    if date_admin is None or len(date_admin) == 0:
        await message.answer('На данный момент нет доступных дат')
        await state.clear()
    else:
        await message.answer('выберите дату:', reply_markup=get_admin_dates_ikb(date_admin))


@client_router.callback_query(NewOrder.date_client, client_cb.filter(F.action == "date_client"))
async def date_select_handler(query: CallbackQuery, callback_data: client_cb, state: FSMContext):
    date_client = callback_data.data_id
    await state.update_data(date_client=date_client)
    await query.answer()
    await state.set_state(NewOrder.phone)
    await query.message.answer('Введите ваш номер телефона', reply_markup=cancel_buttons)


@client_router.message(NewOrder.phone)
async def add_service(message: types.Message, state: FSMContext, bot: Bot):
    phone = message.text
    await state.update_data(phone=phone)
    if message.from_user.id != int(os.getenv('SUDO_ID')):
        await message.answer('Вы записаны, как только мастер будет свободен, он с вами свяжется!\n'
                             'Возникли вопросы?\n'
                             ' Напишите мастеру --> @verasok83', reply_markup=start_buttons)
    else:
        await message.answer('Вы на главном меню', reply_markup=admin_buttons)
    await db.add_item(state)
    await state.clear()

    try:
        await bot.send_message(chat_id=int(os.getenv('NOTICE_ID')), text='К вам новый клиент')
    except (telegram.error.BadRequest, aiogram.exceptions.TelegramNotFound) as e:
        print('При отправке сообщения произошла ошибка:', e)



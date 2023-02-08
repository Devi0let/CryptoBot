from aiogram import types, Dispatcher
from Keyboards import Client_keyboard
from Data_base import sqlite_db


async def start(message: types.Message):
    sql_user_id = await sqlite_db.sql_read_user(message.from_user.id)
    if message.from_user.id == sql_user_id[0][0]:
        mess = f'Привет, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
        await message.answer(mess, parse_mode='html', reply_markup=Client_keyboard.client_markup)
    else:
        await sqlite_db.sql_add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
        mess = f'Привет, ты написал мне впервые,' \
               f' <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
        await message.answer(mess, parse_mode='html', reply_markup=Client_keyboard.client_markup)


async def my_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(my_id, commands=['id'])

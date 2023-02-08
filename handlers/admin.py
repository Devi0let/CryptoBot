from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from GeckoApi import Crypto_get
from Data_base import sqlite_db
from aiogram.dispatcher.filters import Text
from Keyboards import Admin_keyboard, Client_keyboard
from sqlite3 import IntegrityError
from config import ID

global ID


class FSMAdmin(StatesGroup):
    name = State()


class FSMAdmin2(StatesGroup):
    name = State()


async def stock_buttons(message: types.Message):
    await sqlite_db.stock_keyboards()
    await message.answer('Кнопки возвращены к заводским настройкам.', reply_markup=Admin_keyboard.admin_markup)


async def admin_panel(message: types.Message):
    if message.from_user.id in ID:
        await message.answer('Добро пожаловать, Администратор', reply_markup=Admin_keyboard.admin_markup)


async def key_add(message: types.Message):
    if message.from_user.id in ID:
        await FSMAdmin.name.set()
        inkb = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='Отмена',
                                                                                      callback_data='Cancel'))
        await message.answer('Напишите название валюты', reply_markup=inkb)


async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        price = await Crypto_get.crypto_price(message.text)
        if price is None:
            await message.answer('Валюта не найдена, попробуйте ещё раз...', reply_markup=Admin_keyboard.admin_markup)
        else:
            async with state.proxy() as data:
                data['name'] = message.text.lower().capitalize()
            try:
                await sqlite_db.sql_add_key_command(state)
                await message.answer('Кнопка успешно добавлена!', reply_markup=Admin_keyboard.admin_markup)
            except IntegrityError:
                await message.answer('Валюта уже есть в списке, поппробуйте другую.',
                                     reply_markup=Admin_keyboard.admin_markup)
        await state.finish()


async def key_delete(message: types.Message):
    if message.from_user.id in ID:
        await FSMAdmin2.name.set()
        clkey = Client_keyboard.client_markup
        await message.answer('Выберете что хотите удалить...', reply_markup=clkey)


async def name_delete(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['name'] = message.text.lower().capitalize()
        btn1 = types.InlineKeyboardButton(text='Подтвердить', callback_data='Confirm')
        btn2 = types.InlineKeyboardButton(text='Отмена', callback_data='Cancel')
        inkb = types.InlineKeyboardMarkup(row_width=2).add(btn1, btn2)
        await message.answer(f'Вы точно хотите удалить <b>{message.text.capitalize()}</b>?', parse_mode='html',
                             reply_markup=inkb)


async def confirm_call(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await sqlite_db.sql_delete_key_command(state)
        await state.finish()
        await callback.message.answer('Действие успешно выполнено.', reply_markup=Admin_keyboard.admin_markup)
    await callback.answer()


async def cancel_call(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await callback.message.answer('Действие успешно отменено.', reply_markup=Admin_keyboard.admin_markup)
        await state.finish()
    await callback.answer()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands=['Admin'])
    dp.register_message_handler(stock_buttons, commands=['Stock'])
    dp.register_message_handler(key_add, Text(equals='Добавить кнопку', ignore_case=True), state=None)
    dp.register_message_handler(key_delete, Text(equals='Удалить кнопку', ignore_case=True), state=None)
    dp.register_message_handler(name_delete, state=FSMAdmin2.name)
    dp.register_callback_query_handler(confirm_call, text='Confirm', state="*")
    dp.register_callback_query_handler(cancel_call, text='Cancel', state="*")
    dp.register_message_handler(load_name, state=FSMAdmin.name)

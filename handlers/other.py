from aiogram import types, Dispatcher
from GeckoApi import Crypto_get
from Keyboards import Client_keyboard


# @dp.message_handler(content_types=['text'])
async def other_messages_handler(message: types.Message):
    msg = message.text.lower()
    price = await Crypto_get.crypto_price(msg)
    if price is None:
        await message.answer('Валюта не найдена, попробуйте ещё раз.', reply_markup=Client_keyboard.client_markup)
    else:
        await message.answer(f'Цена валюты <b>{message.text}:\n<u>{price}</u> ₽</b>', parse_mode='html',
                             reply_markup=Client_keyboard.client_markup)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(other_messages_handler)

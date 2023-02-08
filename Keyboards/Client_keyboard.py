from aiogram import types

client_markup = None


def new_markup():
    global client_markup
    client_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)


def button_create(keys):
    btn = types.KeyboardButton(text=keys)
    client_markup.insert(btn)

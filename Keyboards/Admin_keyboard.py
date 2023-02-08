from aiogram import types

admin_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn1 = types.KeyboardButton('Добавить кнопку')
btn2 = types.KeyboardButton('Удалить кнопку')
btn3 = types.KeyboardButton('/Stock')
btn4 = types.KeyboardButton('/Start')
admin_markup.add(btn1, btn2, btn3, btn4)

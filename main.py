from aiogram import executor
from create_bot import dp
from Data_base import sqlite_db
from handlers import client, admin, other


async def on_startup(_):
    print('Bot now online!')
    sqlite_db.sql_start()
    await sqlite_db.sql_keys_read()

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

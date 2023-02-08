import sqlite3 as sq
from Keyboards import Client_keyboard


def sql_start():
    global base, cur
    base = sq.connect('Cryptobot.db')
    cur = base.cursor()
    if base:
        print('Data base connected!')
    base.execute('CREATE TABLE IF NOT EXISTS people(id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS keyboards(name TEXT PRIMARY KEY)')
    base.commit()


async def sql_read_user(id):
    return cur.execute(f"SELECT id FROM people WHERE id={id}").fetchall()


async def sql_add_user(id, f_n, s_n):
    cur.execute(f"INSERT INTO people VALUES ({id}, '{f_n}', '{s_n}')")
    base.commit()

async def sql_keys_read():
    Client_keyboard.new_markup()
    for keys in cur.execute('SELECT * FROM keyboards').fetchall():
        Client_keyboard.button_create(keys[0])


async def stock_keyboards():
    cur.execute('DROP TABLE keyboards')
    cur.execute('CREATE TABLE keyboards(name TEXT PRIMARY KEY)')
    cur.execute("INSERT INTO keyboards VALUES ('Bitcoin')")
    cur.execute("INSERT INTO keyboards VALUES ('Dogecoin')")
    cur.execute("INSERT INTO keyboards VALUES ('Asd')")
    cur.execute("INSERT INTO keyboards VALUES ('Ethereum')")
    base.commit()
    await sql_keys_read()


async def sql_add_key_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO keyboards VALUES (?)', tuple(data.values()))
        base.commit()
        await sql_keys_read()


async def sql_delete_key_command(state):
    async with state.proxy() as data:
        cur.execute('DELETE FROM keyboards WHERE name=?', tuple(data.values()))
        base.commit()
        await sql_keys_read()

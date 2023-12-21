from aiogram import types, Dispatcher
from connection import main_sticker, bot
import time, sqlite3, logging

# @dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_first_name = message.from_user.first_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    conn = sqlite3.connect('DATABASE.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO logs (user, time) VALUES (?, ?)', (user_full_name, time.asctime())) #here you insert user`s info into the DataBase File
    conn.commit()
    conn.close()

    # keyboard
    markup = await normal_keyboard_markup()

    await message.delete()
    await bot.send_sticker(message.chat.id, sticker=main_sticker)
    await message.answer(f'Hi, {user_first_name}!\nMy name is <b>ENTER_YOUR_NAME</b>)', #<---- ENTER YOUR NAME HERE
                         parse_mode='HTML', reply_markup=markup)


async def normal_keyboard_markup():
    #default keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Hi!")
    item2 = types.KeyboardButton("Who are you?")
    item3 = types.KeyboardButton("/gpt")
    markup.add(item1, item2, item3)
    return markup


async def gpt_keyboard_markup():
    #gpt keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/cancel")
    markup.add(item1)
    return markup


def register_handlers_buttons(dp : Dispatcher):
    dp.register_message_handler(welcome, commands=['start'])

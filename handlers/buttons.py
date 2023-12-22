# buttons.py: Manages the keyboard button layouts and their responses for user interactions on Telegram.

# Import necessary modules from aiogram.
from aiogram import types, Dispatcher
from connection import main_sticker, bot
import time, sqlite3, logging

# Welcome message handler for the /start command.
async def welcome(message: types.Message):
    # Log user info and insert into the database.
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_first_name = message.from_user.first_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    conn = sqlite3.connect('DATABASE.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO logs (user, time) VALUES (?, ?)', (user_full_name, time.asctime()))
    conn.commit()
    conn.close()

    # Set up and send the welcome message with a default keyboard layout.
    markup = await normal_keyboard_markup()
    await message.delete()
    await bot.send_sticker(message.chat.id, sticker=main_sticker)
    await message.answer(f'Hi, {user_first_name}!\nMy name is <b>ENTER_YOUR_NAME</b>', parse_mode='HTML', reply_markup=markup)

# Function to create a normal keyboard layout.
async def normal_keyboard_markup():
    # Define and return a simple reply keyboard with buttons.
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Hi!")
    item2 = types.KeyboardButton("Who are you?")
    item3 = types.KeyboardButton("/gpt")
    markup.add(item1, item2, item3)
    return markup

# Function to create a keyboard layout for GPT-3 conversation.
async def gpt_keyboard_markup():
    # Define and return a keyboard layout for GPT-3 interactions.
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/cancel")
    markup.add(item1)
    return markup

# Function to register button handlers.
def register_handlers_buttons(dp : Dispatcher):
    # Register the /start command handler.
    dp.register_message_handler(welcome, commands=['start'])

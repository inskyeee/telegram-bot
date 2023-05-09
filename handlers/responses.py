from connection import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3

class Form(StatesGroup):
    waiting_for_answer = State()


# @dp.message_handler(content_types=['text'])
async def replies(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        conn = sqlite3.connect('DATABASE.db') #Here you connect to the Database, so code will insert a new text message that bot had never faced before
        cursor = conn.cursor()            #But if the bot has previously encountered it, it will respond with a reply from DateBase
        cursor.execute('SELECT reply FROM messages WHERE message = ?', (message.text,))
        row = cursor.fetchone()
        if row is not None:
            await message.answer(row[0])
        else:
            await Form.waiting_for_answer.set()
            async with state.proxy() as data:
                data['first_rep'] = message.text
            send = await message.answer(
                "Sorry, but I've never come across a message like that before. How should I respond to it??")
            await state.update_data(previous_message=send.message_id)
        conn.close()


# @dp.message_handler(state=Form.waiting_for_answer, content_types=['text'])
async def process_new_reply(message: types.Message, state: FSMContext):
    data = await state.get_data()
    first_rep = data['first_rep']
    reply = message.text
    conn = sqlite3.connect('DATABASE.db') #In this function bot takes the reply and insert it in the DataBase
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO messages (message, reply) VALUES (?, ?)', (first_rep, reply))
    conn.commit()
    await message.answer("OK, I'll keep that in mind.")
    await state.finish()
    conn.close()


def register_handlers_responses(dp : Dispatcher):
    dp.register_message_handler(replies, content_types=['text'])
    dp.register_message_handler(process_new_reply, state=Form.waiting_for_answer, content_types=['text'])
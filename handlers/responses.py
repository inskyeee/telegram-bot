# responses.py: Manages responses to user inputs, storing and retrieving interactions from the database.

# Import necessary modules from aiogram and sqlite3.
from connection import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3

# Define states for handling new user responses.
class Form(StatesGroup):
    waiting_for_answer = State()

# Handler for responding to user text messages.
async def replies(message: types.Message, state: FSMContext):
    # Check if the message is from a private chat.
    if message.chat.type == 'private':
        # Connect to the database and look for a known response.
        conn = sqlite3.connect('DATABASE.db')
        cursor = conn.cursor()
        cursor.execute('SELECT reply FROM messages WHERE message = ?', (message.text,))
        row = cursor.fetchone()
        if row is not None:
            # Send a known reply from the database.
            await message.answer(row[0])
        else:
            # Start a new state for handling unknown messages.
            await Form.waiting_for_answer.set()
            async with state.proxy() as data:
                data['first_rep'] = message.text
            send = await message.answer("Sorry, but I've never come across a message like that before. How should I respond to it??")
            await state.update_data(previous_message=send.message_id)
        conn.close()

# Handler for processing new user replies for unknown messages.
async def process_new_reply(message: types.Message, state: FSMContext):
    # Retrieve the original message and the user's new reply.
    data = await state.get_data()
    first_rep = data['first_rep']
    reply = message.text
    # Save the new reply to the database.
    conn = sqlite3.connect('DATABASE.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO messages (message, reply) VALUES (?, ?)', (first_rep, reply))
    conn.commit()
    await message.answer("OK, I'll keep that in mind.")
    await state.finish()
    conn.close()

# Function to register response handlers.
def register_handlers_responses(dp : Dispatcher):
    # Register handlers for text messages and unknown replies.
    dp.register_message_handler(replies, content_types=['text'])
    dp.register_message_handler(process_new_reply, state=Form.waiting_for_answer, content_types=['text'])

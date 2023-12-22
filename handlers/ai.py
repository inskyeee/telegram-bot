# ai.py: Handles AI-related interactions using OpenAI's GPT-3 for conversation.

# Import necessary modules from aiogram and openai.
import openai
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .buttons import gpt_keyboard_markup, normal_keyboard_markup

# State class for maintaining conversation states with GPT-3.
class Form(StatesGroup):
    gpt = State()

# Function to get a response from GPT-3 based on the user's input.
async def get_gpt_response(prompt):
    # Generate a completion using OpenAI's GPT-3 model.
    completions = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=2048,
        top_p=0.7,
        n=1,
        stop=None,
        frequency_penalty=0,
        temperature=1,
    )
    return completions.choices[0].text.strip()

# Function to update the conversation prompt for GPT-3.
async def update_prompt(user_id, user_message, current_prompt=None):
    # Format the prompt to include the user's message and identify the conversation.
    if current_prompt is None:
        return f"Conversation with user {user_id}:\nUser: {user_message}\nAI:"
    else:
        return f"{current_prompt}\nUser: {user_message}\nAI:"

# Handler for starting a conversation with the GPT-3 model.
async def gpt_conversation(message: types.Message, state: FSMContext):
    # Set up the keyboard and send an initial message to the user.
    markup = await gpt_keyboard_markup()
    await message.answer("Hi, I'm ChatGPT! What would you like to talk about?\nIf you want to end the conversation, just text me:\n /cancel",
                          reply_markup=markup)
    await Form.gpt.set()
    await state.update_data(prompt="")

# Handler for canceling the GPT-3 conversation.
async def cancel_gpt_conversation(message: types.Message, state: FSMContext):
    # Finish the current state and return to the normal conversation mode.
    await state.finish()
    markup = await normal_keyboard_markup()
    await message.answer("The conversation is over", reply_markup=markup)

# Handler for processing replies in the GPT-3 conversation.
async def gpt_reply(message: types.Message, state: FSMContext):
    # Update the prompt and get a response from GPT-3.
    async with state.proxy() as data:
        current_prompt = data.get("prompt", "")
        user_id = message.from_user.id
        user_message = message.text
        prompt = await update_prompt(user_id, user_message, current_prompt)
        message_text = await get_gpt_response(prompt)
        await message.answer(message_text)
        await state.update_data(prompt=prompt)

# Function to register all handlers related to AI/GPT-3.
def register_handlers_ai(dp: Dispatcher):
    # Register commands and message handlers for GPT-3 conversation.
    dp.register_message_handler(gpt_conversation, commands=['gpt'])
    dp.register_message_handler(cancel_gpt_conversation, commands=['cancel'], state=Form.gpt)
    dp.register_message_handler(gpt_reply, state=Form.gpt, content_types=types.ContentTypes.TEXT)

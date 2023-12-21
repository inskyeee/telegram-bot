import openai
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .buttons import gpt_keyboard_markup, normal_keyboard_markup

class Form(StatesGroup):
    gpt = State()

async def get_gpt_response(prompt):
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

async def update_prompt(user_id, user_message, current_prompt=None):
    if current_prompt is None:
        return f"Conversation with user {user_id}:\nUser: {user_message}\nAI:"
    else:
        return f"{current_prompt}\nUser: {user_message}\nAI:"

async def gpt_conversation(message: types.Message, state: FSMContext):
    markup = await gpt_keyboard_markup()
    await message.answer("Hi, I'm ChatGPT! What would you like to talk about?\nIf you suddenly want to end the conversation with me, just text me:\n /cancel",
                          reply_markup=markup)
    await Form.gpt.set()
    await state.update_data(prompt="")

async def cancel_gpt_conversation(message: types.Message, state: FSMContext):
    await state.finish()
    markup = await normal_keyboard_markup()
    await message.answer("The conversation is over", reply_markup=markup)
    

async def gpt_reply(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        current_prompt = data.get("prompt", "")
        user_id = message.from_user.id
        user_message = message.text
        prompt = await update_prompt(user_id, user_message, current_prompt)
        message_text = await get_gpt_response(prompt)
        await message.answer(message_text)
        await state.update_data(prompt=prompt)


def register_handlers_ai(dp: Dispatcher):
    dp.register_message_handler(gpt_conversation, commands=['gpt'])
    dp.register_message_handler(cancel_gpt_conversation, commands=['cancel'], state=Form.gpt)
    dp.register_message_handler(gpt_reply, state=Form.gpt, content_types=types.ContentTypes.TEXT)

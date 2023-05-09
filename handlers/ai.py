import openai
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    gpt = State()


# @dp.message_handler(commands=['gpt'])
async def gpt_conversation(message: types.Message):
    await message.answer("Hi, I'm ChatGPT! What would you like to talk about?\nIf you suddenly want to end the conversation with me, just text me:\n /cancel")
    await Form.gpt.set()


# @dp.message_handler(commands=['cancel'], state=Form.gpt)
async def cancel_gpt_conversation(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("The conversation is over")


# @dp.message_handler(state=Form.gpt, content_types=types.ContentTypes.TEXT)
async def gpt_reply(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        prompt = f"Conversation with user {message.from_user.id}:\nUser: {message.text}\nAI:"
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
        message_text = completions.choices[0].text.strip()
        await message.answer(message_text)

def register_handlers_ai(dp : Dispatcher):
    dp.register_message_handler(gpt_conversation, commands=['gpt'])
    dp.register_message_handler(cancel_gpt_conversation, commands=['cancel'], state=Form.gpt)
    dp.register_message_handler(gpt_reply, state=Form.gpt, content_types=types.ContentTypes.TEXT)
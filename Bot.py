import os
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from connection import dp
from handlers import ai, buttons, other, responses


class Form(StatesGroup):
    waiting_for_answer = State()
    gpt = State()


async def on_startup(_):
    if not os.getenv('OPEN_AI_TOKEN'):
        raise ValueError('OPEN_AI_TOKEN is not provided')
    print('Bot is running!')


buttons.register_handlers_buttons(dp)
ai.register_handlers_ai(dp)
responses.register_handlers_responses(dp)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

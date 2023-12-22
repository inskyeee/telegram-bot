# connection.py: Establishes and configures the bot's connection and dispatcher.
# Sets up logging and API keys for interactions.

import logging, openai, os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Initialize and configure the bot with the provided API token.
bot = Bot(token=os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

# Set the API key for OpenAI.
openai.api_key = os.getenv('OPEN_AI_TOKEN')
main_sticker = "WRITE_STICKER_ID" # Sticker ID for bot responses.

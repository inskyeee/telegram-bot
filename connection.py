import logging, openai, os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
openai.api_key = os.getenv('OPEN_AI_TOKEN')
main_sticker = "WRITE_STICKER_ID" #<----- Write Sticker Id Here

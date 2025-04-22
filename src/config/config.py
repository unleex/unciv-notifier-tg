from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
# from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env


env =  Env()
env.read_env()
BOT_TOKEN = env('BOT_TOKEN')
ADMIN_IDS: list = env.list('ADMIN_IDS')
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
# redis = Redis(host='localhost')
# storage = RedisStorage(redis=redis)
storage = MemoryStorage() 
dp = Dispatcher(storage=storage)
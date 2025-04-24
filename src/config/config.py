from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, Redis
from environs import Env
import gigachat
from llm.llm import LLM
from prompts.prompts import PROMPTS_RU

prompts = PROMPTS_RU

env =  Env()
env.read_env()
BOT_TOKEN = env('BOT_TOKEN')
ADMIN_IDS: list[int] = env.list('ADMIN_IDS')
GIGACHAT_API_TOKEN = env('GIGACHAT_API_TOKEN')
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
redis = Redis(host='amvera-unleex-run-redis')
storage = RedisStorage(redis=redis) 
dp = Dispatcher(storage=storage)
llm = LLM(
    credentials=GIGACHAT_API_TOKEN,
    verify_ssl_certs=False,
    system_prompt=prompts["news_system"],
    max_tokens=300
)

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import re
import asyncio

from aiogram import Bot, F, Router
from aiogram.filters import BaseFilter, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from config.config import bot
from keyboards.keyboards import create_civ_choosing_kb
from lexicon.lexicon import LEXICON_EN
from mainloop import mainloop
from prompts.prompts import PROMPTS_RU
from states.states import FSMStates
from unciv.getdata import get_civs



rt = Router()
lexicon = LEXICON_EN
prompts = PROMPTS_RU



@rt.message(Command("get_turn"), StateFilter(FSMStates.playing))
async def get_turn(msg: Message, state: FSMContext):
    data = (await state.get_data())
    await mainloop.update(
        bot, 
        msg.chat.id,
        civ_to_player=data["players"],
        last_turn=-1,
        last_civ=None,
        get_news_cycle_end=False,
        game_id=data["game_id"]
    )

@rt.message(Command("hullo"), StateFilter(FSMStates.playing))
async def hullo(msg: Message, state: FSMContext):
    for task in asyncio.all_tasks():
        if task.get_name() == "mainloop":
            task.cancel()
    async def check_status():
        return (await state.get_data()).get("running", False)
    data = await state.get_data()
    asyncio.create_task(
        mainloop.mainloop(
            bot=bot,
            game_id=data["game_id"],
            chat_id=msg.chat.id,
            civ_to_player=data["players"],
            status_checker=check_status,
        ),
        name="mainloop"
    )
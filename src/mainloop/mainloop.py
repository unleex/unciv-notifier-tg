import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


import base64
import ctypes
import gzip
import json
import time

import requests

from aiogram import Bot, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from config.config import bot, llm
from lexicon.lexicon import LEXICON_EN
from llm.llm import LLM
from states.states import FSMStates
from unciv import getdata

rt = Router()
lexicon = LEXICON_EN


def get_news(
    news_data: dict[str, list],
    model: LLM
):
    all_news: dict[str, str] = {}
    for civ, data in news_data.items():
        all_news[civ] = model.prompt('\n'.join(data))
    return all_news


async def update(
    bot: Bot,
    chat_id, 
    game_id,
    civ_to_player,
    last_turn,
    last_civ,
    get_news_cycle_end: bool = True
):
    server_response = requests.get(f"https://uncivserver.xyz/files/{game_id}_Preview")
    data = json.loads(
        gzip.decompress(base64.b64decode(server_response.content)).decode("utf-8")
    )
    if "turns" not in data:
        await bot.send_message(chat_id, lexicon["notification_no_turns"])
    turn = data["turns"]
    country_turn = data["currentPlayer"]

    if last_civ != country_turn:
        message = lexicon["notification"] % (turn, str(civ_to_player[country_turn]))
        await bot.send_message(chat_id, message)
        if last_turn != turn and get_news_cycle_end:
            await bot.send_message(chat_id=chat_id, text=lexicon['generating_news'])
            news = get_news(
                getdata.get_notifications(
                    gameid=game_id
                ),
                model=llm
            )
            news_text = ""
            for civ, news in news.items():
                news_text += f"{civ}:\n{news}\n\n"

            await bot.send_message(chat_id=chat_id, text=lexicon['news'] % news_text)

    last_turn = turn
    last_civ = country_turn
    return last_turn, last_civ

async def mainloop(
        bot,
        chat_id, 
        game_id,
        status_checker,
        civ_to_player,
        timeout=60
        ):
    last_turn = None
    last_civ = None
    last_time = time.time()
    while await status_checker():
        now = time.time()
        if now - last_time > timeout:
            last_time = now
            last_turn, last_civ = await update(
                bot=bot, 
                chat_id=chat_id, 
                game_id=game_id, 
                civ_to_player=civ_to_player, 
                last_turn=last_turn,
                last_civ=last_civ
                )
    
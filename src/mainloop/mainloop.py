import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import asyncio
import base64
import gzip
import json

import requests

from aiogram import Bot, Router
from config.config import llm
from lexicon.lexicon import LEXICON_EN
from llm.llm import LLM
from unciv import getdata
from prompts.prompts import PROMPTS_RU

rt = Router()
lexicon = LEXICON_EN
prompts = PROMPTS_RU

def get_news(
    news_data: dict[str, list],
    model: LLM
):
    all_news: dict[str, str] = {}
    for civ, data in news_data.items():
        all_news[civ] = model.prompt(prompts["get_news"] % civ + '\n' + '\n'.join(data))
    return all_news


async def update(
    bot: Bot,
    chat_id, 
    game_id,
    civ_to_player,
    last_turn,
    last_civ,
    get_news_cycle_end: bool = True
) -> tuple:
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
            for civ, news in news.items():
                await bot.send_message(chat_id=chat_id, text=lexicon['news'] % news)


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
    while await status_checker():
        last_turn, last_civ = await update(
            bot=bot, 
            chat_id=chat_id, 
            game_id=game_id, 
            civ_to_player=civ_to_player, 
            last_turn=last_turn,
            last_civ=last_civ
            )
        asyncio.sleep(timeout)
    
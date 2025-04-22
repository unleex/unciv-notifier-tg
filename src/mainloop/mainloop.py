import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


import time

from aiogram import Router, Bot
from aiogram.filters import StateFilter, CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from lexicon.lexicon import LEXICON_EN
from states.states import FSMStates
from config.config import bot
import requests
import json
import gzip
import base64
import ctypes

rt = Router()
lexicon = LEXICON_EN

async def update(
    bot: Bot,
    chat_id, 
    game_id,
    civ_to_player,
    last_turn
):
    server_response = requests.get(f"https://uncivserver.xyz/files/{game_id}_Preview")
    data = json.loads(
        gzip.decompress(base64.b64decode(server_response.content)).decode("utf-8")
    )
    print(data)
    if "turns" not in data:
        await bot.send_message(chat_id, lexicon["notification_no_turns"])
    turn = data["turns"]
    country_turn = data["currentPlayer"]

    if last_turn != turn:
        message = lexicon["notification"] % (turn, str(civ_to_player[country_turn]))
        await bot.send_message(chat_id, message)
        last_turn = turn
    return last_turn

async def mainloop(
        bot,
        chat_id, 
        game_id,
        status_checker,
        civ_to_player,
        timeout=60
        ):
    last_turn = None
    last_time = time.time()
    while await status_checker():
        now = time.time()
        if now - last_time > timeout:
            last_time = now
            last_turn = await update(
                bot=bot, 
                chat_id=chat_id, 
                game_id=game_id, 
                civ_to_player=civ_to_player, 
                last_turn=last_turn
                )
    
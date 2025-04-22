import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import re 
from mainloop import mainloop
from config.config import bot

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from keyboards.keyboards import create_civ_choosing_kb
from lexicon.lexicon import LEXICON_EN
from states.states import FSMStates
from unciv.getdata import get_civs
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class ManualCivAssignation(BaseFilter):
    async def __call__(self,  msg: Message) -> bool:
        return len(msg.text.split('-')) == 2

rt = Router()
lexicon = LEXICON_EN

@rt.message(Command("start"), StateFilter(default_state))
async def start(msg: Message, state: FSMContext):
    await FSMStates.clear_chat_state(msg.chat.id)
    await msg.answer(lexicon["init_game"])
    await state.set_state(FSMStates.getting_game_id)

@rt.message(StateFilter(FSMStates.getting_game_id))
async def assigning_civs(msg: Message, state: FSMContext):
    text = msg.text.strip()
    if re.fullmatch((r'[\w]+-'*5)[:-1], text):
        await FSMStates.set_chat_data(msg.chat.id, {"game_id": text})
        civs = get_civs(text)
        kb = create_civ_choosing_kb(
            civs
        )
        await msg.answer(
            lexicon["waiting_for_assigning_civs"],
            reply_markup=kb
        )
        await FSMStates.set_chat_state(msg.chat.id, FSMStates.waiting_for_assigning_civs)
        await FSMStates.set_chat_data(
            msg.chat.id, 
            {
                "players": {
                    civ: None 
                    for civ in civs
                }
            }
        )
    else:
        await msg.answer(lexicon["invalid_game_id"])

@rt.callback_query(
        F.data.endswith("civ_chosen"), 
        StateFilter(FSMStates.waiting_for_assigning_civs)
)
async def choose_civ(clb: CallbackQuery, state: FSMContext):
    civ = clb.data.replace("_civ_chosen", "")  # type: ignore[union-attr]
    kb = clb.message.reply_markup  # type: ignore[union-attr]
    statedata = (await state.get_data())
    players = statedata["players"]
    player_to_civ = dict(zip(
        players.values(), 
        players.keys()
        ))
    previous_civ = player_to_civ.get(clb.from_user.username, None)
    if previous_civ:
        players[previous_civ] = None
    players[civ] = clb.from_user.username
    await FSMStates.set_chat_data(clb.message.chat.id, {"players": players})  # type: ignore[union-attr]
    for button_row in kb.inline_keyboard:  # type: ignore[union-attr]
        button = button_row[0]
        if previous_civ and previous_civ in button.text:
            button.text = (
                button.callback_data.replace("_civ_chosen","")
            )
        if button.text == civ:
            button.text = f"{civ} - {clb.from_user.username}"
    await clb.message.edit_reply_markup(
        reply_markup=kb
    )
    await start_game_if_ready(clb.message.chat.id, state, bot)


async def start_game_if_ready(chat_id, state, bot: Bot):
    statedata = (await state.get_data())
    players = statedata["players"]
    if all([data is not None for data in players.values()]):
        await bot.send_message(chat_id, lexicon["starting"])
        await FSMStates.set_chat_state(chat_id, FSMStates.playing)
        await FSMStates.set_chat_data(chat_id, {"running": True})
        async def check_status():
            return (await state.get_data()).get("running", False)
        civ_to_player = players
        await mainloop.mainloop(
            bot=bot, 
            chat_id=chat_id, 
            game_id=statedata["game_id"],
            civ_to_player=civ_to_player,
            status_checker=check_status,
            timeout=60
        )



        
@rt.message(Command("stop"), StateFilter(FSMStates.playing))
async def stop(msg: Message):
    await msg.answer(lexicon["stopping"])
    await FSMStates.clear_chat(msg.chat.id)

@rt.message(StateFilter(FSMStates.waiting_for_assigning_civs), ManualCivAssignation())
async def manual_assign_civ(msg: Message, state: FSMContext):
    civ, user = msg.text.split('-')
    civ = civ.strip()
    user = user.strip()
    statedata = (await state.get_data())
    players = statedata["players"]
    if civ not in players:
        await msg.reply(lexicon["invalid_civ"] % civ)
        return
    for assigned_civ, username in players.items():
        if username == user:
            players[assigned_civ] = None
            break
    players[civ] = user
    await FSMStates.set_chat_data(msg.chat.id, {"players": players})
    await msg.reply(lexicon["manually_assigned_civ"] % (user, civ))
    await start_game_if_ready(msg.chat.id, state, bot)

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from lexicon.lexicon import LEXICON_EN
from states.states import FSMStates


rt = Router()
lexicon = LEXICON_EN

@rt.message(Command("reload"))
async def reload(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("еба")

@rt.message(Command("debug"))
async def debug(msg: Message, state: FSMContext):
    ret = [
        "chat_states: " + str(await FSMStates.get_chat_states(msg.chat.id)),
        "data: " + str(await state.get_data()),
    ]
    await msg.answer('\n'.join(ret))
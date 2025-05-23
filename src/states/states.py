import json

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey

from config.config import bot, storage

class FSMStates(StatesGroup):
    getting_game_id = State()
    waiting_for_assigning_civs = State()
    playing = State()
    
    @staticmethod
    async def set_chat_state(chat_id: int, state: State | None):
        with open("src/db/chat_database.json") as f:
            db = json.load(f)
        for user_id in db[str(chat_id)]["users"]:
            new_storage_key = StorageKey(int(bot.id), int(chat_id), int(user_id))
            ctx = FSMContext(storage,new_storage_key)
            await ctx.set_state(state)
    
    @staticmethod
    async def set_chat_data(chat_id: int, data: dict, overwrite=False):
        with open("src/db/chat_database.json") as f:
            db = json.load(f)
        for user_id in db[str(chat_id)]["users"]:
            new_storage_key = StorageKey(int(bot.id), int(chat_id), int(user_id))
            ctx = FSMContext(storage,new_storage_key)
            if not overwrite:
                data = (await ctx.get_data()) | data
            await ctx.set_data(data)
    
    @staticmethod 
    async def get_chat_states(chat_id: int):
        states = {}
        with open("src/db/chat_database.json") as f:
            db = json.load(f)
        for user_id in db[str(chat_id)]["users"]:
            new_storage_key = StorageKey(int(bot.id), int(chat_id), int(user_id))
            ctx = FSMContext(storage,new_storage_key)
            states[user_id] = await ctx.get_state()
        return states

    @staticmethod
    async def clear_chat_data(chat_id: int):
        await FSMStates.set_chat_data(chat_id, {}, overwrite=True)

    @staticmethod
    async def clear_chat_state(chat_id: int):
        await FSMStates.set_chat_state(chat_id, None)
    
    @staticmethod
    async def clear_chat(chat_id: int):
        await FSMStates.clear_chat_state(chat_id)
        await FSMStates.clear_chat_data(chat_id)

    @staticmethod
    async def multiset_state(ids: list[int], chat_id: int, state: State | None):
        for user_id in ids:
            new_storage_key = StorageKey(int(bot.id), int(chat_id), int(user_id))
            ctx = FSMContext(storage,new_storage_key)
            await ctx.set_state(state)
    
    @staticmethod
    async def multiset_data(ids: list[int], chat_id: int, data: dict, overwrite=False):
        for user_id in ids:
            new_storage_key = StorageKey(int(bot.id), int(chat_id), int(user_id))
            ctx = FSMContext(storage, new_storage_key)
            if not overwrite:
                data = (await ctx.get_data()) | data
            await ctx.set_data(data)

    @staticmethod 
    async def multiget_states(chat_id: int, ids: list[int]):
        states = {}
        for user_id in ids:
            new_storage_key = StorageKey(int(bot.id), int(chat_id), int(user_id))
            ctx = FSMContext(storage,new_storage_key)
            states[user_id] = await ctx.get_state()
        return states

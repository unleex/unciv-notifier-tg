import asyncio
from config.config import bot, dp
from keyboards.set_menu import set_main_menu
from handlers import game, other_handlers
from middlewares.middlewares import DataBaseAccessor

async def main() -> None:
    await bot.delete_webhook(drop_pending_updates = True)
    await set_main_menu(bot)
    dp.include_router(other_handlers.rt)
    dp.include_router(game.rt)
    dp.update.middleware(DataBaseAccessor())
    print("starting")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
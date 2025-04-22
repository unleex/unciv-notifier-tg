print("1")
import asyncio
from config.config import bot, dp
from keyboards.set_menu import set_main_menu
from handlers import game, other_handlers
from middlewares.middlewares import DataBaseAccessor

async def main() -> None:
    await bot.delete_webhook(drop_pending_updates = True)
    print("9")
    await set_main_menu(bot)
    print("10")
    dp.include_router(other_handlers.rt)
    print("13")
    dp.include_router(game.rt)
    print("15")
    dp.update.middleware(DataBaseAccessor())
    print("starting")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
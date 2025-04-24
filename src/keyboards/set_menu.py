from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(command="start", description="Start notifications!"),
        BotCommand(command="stop", description="Stop notifications"),
        ]
    await bot.set_my_commands(main_menu_commands)

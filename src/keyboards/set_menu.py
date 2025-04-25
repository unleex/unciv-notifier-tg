from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(command="start", description="Start notifications!"),
        BotCommand(command="stop", description="Stop notifications"),
        BotCommand(command="get_turn", description="Get current turn"),
        BotCommand(command="hullo", description="Try to reload if notifications aren't being sent"),
        ]
    await bot.set_my_commands(main_menu_commands)
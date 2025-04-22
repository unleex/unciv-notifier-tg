from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_civ_choosing_kb(civs: list[str]):
    buttons = [InlineKeyboardButton(
        text=civ,
        callback_data=f"{civ}_civ_chosen"
    ) for civ in civs]

    return InlineKeyboardMarkup(
        inline_keyboard=[[button] for button in buttons],
        resize_keyboard=True
    )
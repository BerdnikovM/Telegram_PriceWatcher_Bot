from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def interval_inline_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⏱ 1 мин", callback_data="interval:1"),
                InlineKeyboardButton(text="⏱ 5 мин", callback_data="interval:5"),
            ],
            [
                InlineKeyboardButton(text="⏱ 15 мин", callback_data="interval:15"),
                InlineKeyboardButton(text="⏱ 30 мин", callback_data="interval:30"),
            ],
            [
                InlineKeyboardButton(text="⏱ 60 мин", callback_data="interval:60"),
            ]
        ]
    )


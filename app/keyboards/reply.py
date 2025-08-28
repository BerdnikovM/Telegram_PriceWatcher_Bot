from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

interval_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="5 мин"), KeyboardButton(text="15 мин")],
        [KeyboardButton(text="30 мин"), KeyboardButton(text="60 мин")]
    ],
    resize_keyboard=True
)


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/add")],
        [KeyboardButton(text="/list")],
        [KeyboardButton(text="/help")],
    ],
    resize_keyboard=True,   # подгоняет клавиатуру под экран
    one_time_keyboard=False # клавиатура всегда доступна
)

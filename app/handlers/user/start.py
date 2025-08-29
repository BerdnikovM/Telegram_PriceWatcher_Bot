from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.db import crud
from app.keyboards.reply import main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    user = await crud.get_user_by_telegram_id(message.from_user.id)

    if not user:
        await crud.create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
        text = "👋 Привет! Я PriceWatcherBot.\n\nЯ помогу отслеживать цены на товары.\n\n"
    else:
        text = "👋 С возвращением! Ты уже зарегистрирован."

    # Всегда показываем меню
    await message.answer(
        f"{text}\n\n"
        "📌 Доступные команды:\n"
        "• /add — добавить товар\n"
        "• /list — список отслеживаемых\n"
        "• /help — помощь",
        reply_markup=main_menu
    )

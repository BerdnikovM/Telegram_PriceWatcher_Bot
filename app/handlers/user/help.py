# app/handlers/user/help.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🛠 <b>Доступные команды:</b>\n"
        "/start — начать и зарегистрироваться\n"
        "/help — помощь\n"
        "/add — добавить ссылку на товар\n"
        "/list — список отслеживаемых\n"
        "/remove — удалить товар\n"
        "/settings — настройки уведомлений\n"
    )

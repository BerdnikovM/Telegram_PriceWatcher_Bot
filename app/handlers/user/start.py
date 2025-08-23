# app/handlers/user/start.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from app.db import crud

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    user = await crud.get_user_by_telegram_id(message.from_user.id)
    if not user:
        await crud.create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
        await message.answer("👋 Привет! Ты зарегистрирован в системе.")
    else:
        await message.answer("👋 С возвращением! Ты уже зарегистрирован.")

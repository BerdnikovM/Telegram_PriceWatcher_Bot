# app/main.py

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from aiogram.client.default import DefaultBotProperties

from app.config import settings
from app.handlers.user import start as user_start
from app.handlers.user import help as user_help
from app.handlers.user import add as user_add

from app.services.scheduler import scheduler, launch_all_price_checks  # <-- наш singleton
import nest_asyncio

nest_asyncio.apply()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(fsm_strategy=FSMStrategy.CHAT)

    dp.include_router(user_start.router)
    dp.include_router(user_help.router)
    dp.include_router(user_add.router)

    # ❗ стартуем именно singleton-планировщик
    scheduler.start()
    await launch_all_price_checks()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# app/db/init_db.py

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings
from app.models.user import User
from app.models.item import WatchedItem
import asyncio


# Создание движка для асинхронной работы с БД
engine = create_async_engine(settings.DATABASE_URL, echo=True)


# Создание всех таблиц на основе моделей
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Таблицы успешно созданы.")


# Ручной запуск
if __name__ == "__main__":
    asyncio.run(init_db())

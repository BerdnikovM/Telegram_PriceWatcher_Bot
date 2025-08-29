# app/db/__init__.py

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from contextlib import asynccontextmanager  # <--- добавь этот импорт

# Асинхронный движок
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
)

# Асинхронная фабрика сессий
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Функция получения сессии (можно использовать через async with)
@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session

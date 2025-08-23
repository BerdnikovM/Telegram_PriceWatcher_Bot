# app/config.py

from pydantic import BaseSettings, AnyHttpUrl
from typing import List
from dotenv import load_dotenv
import os

# Загрузка переменных из .env
load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str
    ADMINS: List[int]

    class Config:
        case_sensitive = True


def parse_admins(admins_raw: str) -> List[int]:
    return [int(admin.strip()) for admin in admins_raw.split(",") if admin.strip().isdigit()]


# Инициализация настроек
settings = Settings(
    BOT_TOKEN=os.getenv("BOT_TOKEN"),
    DATABASE_URL=os.getenv("DATABASE_URL"),
    ADMINS=parse_admins(os.getenv("ADMINS", ""))
)

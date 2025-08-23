# app/config.py

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(...)
    DATABASE_URL: str = Field(...)
    ADMINS: List[int] = Field(...)

    class Config:
        case_sensitive = True


def parse_admins(admins_raw: str) -> List[int]:
    return [int(admin.strip()) for admin in admins_raw.split(",") if admin.strip().isdigit()]


settings = Settings(
    BOT_TOKEN=os.getenv("BOT_TOKEN"),
    DATABASE_URL=os.getenv("DATABASE_URL"),
    ADMINS=parse_admins(os.getenv("ADMINS", ""))
)

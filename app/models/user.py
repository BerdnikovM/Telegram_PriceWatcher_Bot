# app/models/user.py

from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    telegram_id: int = Field(index=True, unique=True)
    username: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


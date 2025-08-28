# app/models/item.py

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from decimal import Decimal
from typing import Optional

class WatchedItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    url: str
    title: Optional[str] = None

    current_price: Optional[Decimal] = None
    threshold_price: Optional[Decimal] = None
    percent_change: Optional[float] = None

    last_checked: Optional[datetime] = None
    is_active: bool = Field(default=True)
    check_interval: int = Field(default=15, description="Частота проверки цены (в минутах)")

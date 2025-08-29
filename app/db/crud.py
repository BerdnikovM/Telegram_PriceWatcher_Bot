from sqlmodel import select, delete, update
from app.models.user import User
from app.models.item import WatchedItem
from app.db import get_session
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

# --- USER ---

async def create_user(telegram_id: int, username: Optional[str] = None) -> User:
    async with get_session() as session:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

async def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    async with get_session() as session:
        result = await session.exec(select(User).where(User.telegram_id == telegram_id))
        return result.first()

# --- WATCHED ITEM ---

async def add_watched_item(
    user_id: int,
    url: str,
    threshold_price: Optional[Decimal] = None,
    percent_change: Optional[float] = None,
    title: Optional[str] = None,
    current_price: Optional[Decimal] = None,
    check_interval: int = 15
) -> WatchedItem:
    async with get_session() as session:
        item = WatchedItem(
            user_id=user_id,
            url=url,
            title=title,
            threshold_price=threshold_price,
            percent_change=percent_change,
            current_price=current_price,
            check_interval=check_interval
        )
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

async def get_items_by_user(user_id: int) -> List[WatchedItem]:
    async with get_session() as session:
        result = await session.exec(select(WatchedItem).where(WatchedItem.user_id == user_id))
        return result.all()

async def get_active_items() -> List[WatchedItem]:
    async with get_session() as session:
        result = await session.exec(select(WatchedItem).where(WatchedItem.is_active == True))
        return result.all()

async def delete_item(item_id: int) -> bool:
    async with get_session() as session:
        result = await session.exec(delete(WatchedItem).where(WatchedItem.id == item_id))
        await session.commit()
        return result.rowcount > 0

async def update_item_threshold(item_id: int, new_price: Decimal) -> bool:
    async with get_session() as session:
        result = await session.exec(
            update(WatchedItem)
            .where(WatchedItem.id == item_id)
            .values(threshold_price=new_price)
        )
        await session.commit()
        return result.rowcount > 0

async def get_item_by_id(item_id: int) -> Optional[WatchedItem]:
    async with get_session() as session:
        item = await session.get(WatchedItem, item_id)
        return item

async def update_current_price(item_id: int, new_price: Decimal) -> bool:
    async with get_session() as session:
        result = await session.exec(
            update(WatchedItem)
            .where(WatchedItem.id == item_id)
            .values(
                current_price=new_price,
                last_checked=datetime.utcnow()
            )
        )
        await session.commit()
        return result.rowcount > 0

async def get_all_active_items() -> List[WatchedItem]:
    async with get_session() as session:
        result = await session.exec(
            select(WatchedItem).where(WatchedItem.is_active == True)
        )
        return result.all()

async def update_last_checked(item_id: int) -> bool:
    async with get_session() as session:
        result = await session.exec(
            update(WatchedItem)
            .where(WatchedItem.id == item_id)
            .values(
                last_checked=datetime.utcnow()
            )
        )
        await session.commit()
        return result.rowcount > 0


async def get_user_by_id(user_id: int) -> Optional[User]:
    async with get_session() as session:
        return await session.get(User, user_id)
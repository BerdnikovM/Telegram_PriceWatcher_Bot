# app/services/scheduler.py

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.db.crud import get_all_active_items, get_item_by_id, update_current_price
from app.services.parser import fetch_price

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.start()

def schedule_price_check(item_id: int, interval: int):
    # id задачи уникален по item
    job_id = f"item_{item_id}"
    # если задача уже есть — заменяем
    scheduler.add_job(
        check_price_for_item,
        'interval',
        minutes=interval,
        args=[item_id],
        id=job_id,
        replace_existing=True,
        coalesce=True,
        misfire_grace_time=60
    )

async def check_price_for_item(item_id: int):
    item = await get_item_by_id(item_id)
    if not item or not item.is_active:
        print(f"[Scheduler] WatchedItem {item_id} не найден или неактивен")
        return

    price, title, method = await fetch_price(item.url)
    print(f"[Scheduler][{method}] {title or 'Нет заголовка'} — {price or 'нет цены'}")

    if price is not None and price != item.current_price:
        print(f"➡️ Цена изменилась для {item.title or item.url}: {item.current_price} → {price}")
        await update_current_price(item_id, price)
    else:
        print("Цена не изменилась.")

def clear_jobs():
    scheduler.remove_all_jobs()


# app/services/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.db.crud import get_all_active_items, get_item_by_id, update_current_price, update_last_checked, get_user_by_telegram_id, get_user_by_id
from app.services.parser import fetch_price
from aiogram import Bot
from app.config import settings

scheduler = AsyncIOScheduler()

def schedule_price_check(item_id: int, interval: int):

    scheduler.add_job(
        check_price_for_item,
        'interval',
        minutes=interval,
        args=[item_id],
        id=f"item_{item_id}",
        replace_existing=True,
        coalesce=True,
        misfire_grace_time=60,
    )

async def check_price_for_item(item_id: int):
    item = await get_item_by_id(item_id)
    if not item or not item.is_active:
        print(f"[Scheduler] WatchedItem {item_id} не найден или неактивен")
        return

    # Обновляем время проверки всегда
    await update_last_checked(item_id)

    price, title, method = await fetch_price(item.url)
    print(f"[Scheduler][{method}] {title or 'Нет заголовка'} — {price or 'нет цены'}")

    if price is not None and price != item.current_price:
        print(f"➡️ Цена изменилась для {item.title or item.url}: {item.current_price} → {price}")
        await update_current_price(item_id, price)

        # Получаем пользователя по FK и шлём на его telegram_id
        user = await get_user_by_id(item.user_id)
        if user and user.telegram_id:
            bot = Bot(token=settings.BOT_TOKEN)
            text = (
                f"🔔 <b>Цена изменилась!</b>\n\n"
                f"<b>{item.title or item.url}</b>\n"
                f"Старая цена: {item.current_price} ₽\n"
                f"Новая цена: {price} ₽"
            )
            try:
                await bot.send_message(user.telegram_id, text, parse_mode="HTML")
            except Exception as e:
                print(f"[Scheduler] Ошибка отправки сообщения: {e}")
            await bot.session.close()
    else:
        print("Цена не изменилась.")


async def launch_all_price_checks():
    items = await get_all_active_items()
    for item in items:
        schedule_price_check(item.id, item.check_interval)
        print(f"[Scheduler] Задача запущена для item_id={item.id}, интервал={item.check_interval} мин.")

def clear_jobs():
    scheduler.remove_all_jobs()

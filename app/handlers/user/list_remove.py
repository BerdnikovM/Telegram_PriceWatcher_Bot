from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from typing import List

from app.db import crud
from app.models.item import WatchedItem

router = Router()


def build_remove_keyboard(item_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Удалить", callback_data=f"rm:{item_id}")]
        ]
    )


def format_item_line(index: int, it: WatchedItem) -> str:
    price = f"{it.current_price} ₽" if it.current_price else "—"
    title = it.title or "(без названия)"
    interval = it.check_interval or "—"
    return (
        f"#{index}\n"
        f"<b>{title}</b>\n"
        f"💰 {price} | ⏱ {interval} мин\n"
        f"🔗 {it.url}"
    )


@router.message(Command("list"))
async def cmd_list(message: Message):
    user = await crud.get_user_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer("Ты ещё не зарегистрирован. Нажми /start.")
        return

    items = await crud.get_items_by_user(user.id)
    if not items:
        await message.answer("Пока нет отслеживаемых товаров. Добавь через /add")
        return

    for idx, it in enumerate(items, start=1):
        text = format_item_line(idx, it)
        kb = build_remove_keyboard(it.id)
        # disable_web_page_preview убирает предпросмотр ссылок
        await message.answer(text, reply_markup=kb, disable_web_page_preview=True)

@router.callback_query(F.data.startswith("rm:"))
async def on_remove_click(call: CallbackQuery):
    try:
        _, raw_id = call.data.split(":", 1)
        item_id = int(raw_id)
    except Exception:
        await call.answer("Некорректный запрос.", show_alert=True)
        return

    item = await crud.get_item_by_id(item_id)
    if not item:
        await call.answer("Запись не найдена.", show_alert=True)
        return

    user = await crud.get_user_by_telegram_id(call.from_user.id)
    if not user or item.user_id != user.id:
        await call.answer("Это не твоё отслеживание.", show_alert=True)
        return

    ok = await crud.delete_item(item_id)
    if ok:
        await call.message.edit_text("Элемент удалён ✅")
    else:
        await call.answer("Не удалось удалить. Попробуй позже.", show_alert=True)

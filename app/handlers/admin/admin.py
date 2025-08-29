import asyncio
import re
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import settings
from app.db import crud
from app.models.user import User

router = Router()

PAGE_SIZE = 10
batch_size = 20
delay = 1


# --- Helpers ---

def build_users_keyboard(page: int, total: int):
    builder = InlineKeyboardBuilder()
    if (page + 1) * PAGE_SIZE < total:
        builder.button(text="▶️ Далее", callback_data=f"users_page_{page + 1}")
    builder.button(text="❌ Выйти", callback_data="users_exit")
    return builder.as_markup()


def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMINS


async def safe_send(bot, user_id, text):
    try:
        await bot.send_message(user_id, text)
        return True
    except (TelegramForbiddenError, TelegramBadRequest):
        logging.warning("Пользователь %s недоступен для рассылки.", user_id)
        return False
    except Exception:
        logging.exception("Ошибка при отправке %s", user_id)
        return False


# --- Commands ---

@router.message(Command("users"))
async def users_count(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔️ У тебя нет прав для этой команды.")

    try:
        users = await crud.get_all_users()

        page = 0
        total = len(users)
        users_page = users[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]

        text = "<b>Пользователи:</b>\n"
        for u in users_page:
            text += f"id: <code>{u.telegram_id}</code> | @{u.username or '-'}\n"
        text += f"\nПоказано {page * PAGE_SIZE + 1}–{page * PAGE_SIZE + len(users_page)} из {total}"

        await message.answer(
            text,
            reply_markup=build_users_keyboard(page, total)
        )
    except Exception:
        logging.exception("Failed to handle /users")
        await message.answer("Не удалось получить список пользователей. Попробуй позже.")


@router.callback_query(F.data.startswith("users_page_"))
async def users_next_page(callback: CallbackQuery):
    try:
        page = int(callback.data.split("_")[-1])
        users = await crud.get_all_users()

        total = len(users)
        users_page = users[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]

        text = "<b>Пользователи:</b>\n"
        for u in users_page:
            text += f"id: <code>{u.telegram_id}</code> | @{u.username or '-'}\n"
        text += f"\nПоказано {page * PAGE_SIZE + 1}–{page * PAGE_SIZE + len(users_page)} из {total}"

        await callback.message.edit_text(
            text,
            reply_markup=build_users_keyboard(page, total)
        )
        await callback.answer()
    except Exception:
        logging.exception("Failed to paginate users")
        await callback.answer("Ошибка при получении страницы.", show_alert=True)


@router.callback_query(F.data == "users_exit")
async def users_exit(callback: CallbackQuery):
    try:
        await callback.message.edit_text("Просмотр пользователей завершён.")
        await callback.answer()
    except Exception:
        logging.exception("Failed to exit user list")
        await callback.answer("Ошибка.", show_alert=True)


@router.message(Command("broadcast"))
async def broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔️ У тебя нет прав для этой команды.")

    try:
        cmd = message.text[len("/broadcast"):].strip()

        ids = None
        text = None

        m = re.search(r'ids\s*=\s*([^\s]+)', cmd)
        if m:
            raw_ids = m.group(1)
            ids = [int(s.strip()) for s in raw_ids.split(",") if s.strip().isdigit()]
            cmd = cmd.replace(m.group(0), '').strip()

        m_text = re.search(r'text\s*=\s*(.+)', cmd)
        if m_text:
            text = m_text.group(1).strip()
        elif not ids:
            text = cmd.strip()
        else:
            return await message.answer("Не найден аргумент text=. Пример:\n/broadcast ids=123,456 text=Сообщение")

        if not text:
            return await message.answer("Текст сообщения не должен быть пустым.")

        users = await crud.get_all_users()
        if ids:
            users = [u for u in users if u.telegram_id in ids]

        count = 0
        failed = []
        for i in range(0, len(users), batch_size):
            batch = users[i:i + batch_size]
            tasks = [safe_send(message.bot, user.telegram_id, text) for user in batch]
            results = await asyncio.gather(*tasks)
            for idx, ok in enumerate(results):
                if ok:
                    count += 1
                else:
                    failed.append(batch[idx].telegram_id)
            await asyncio.sleep(delay)

        reply = f"Сообщение отправлено {count} пользователям."
        if failed:
            reply += "\n❗️ Не удалось доставить:\n" + ", ".join(str(uid) for uid in failed)
        await message.answer(reply)
    except Exception:
        logging.exception("Failed to broadcast message")
        await message.answer("Не удалось выполнить рассылку. Попробуй позже.")


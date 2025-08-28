# app/handlers/user/add.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.services.parser import fetch_price
from app.db import crud
from app.models.user import User
from urllib.parse import urlparse
from app.keyboards.reply import interval_kb

router = Router()


class AddItemState(StatesGroup):
    waiting_for_url = State()
    waiting_for_type = State()
    waiting_for_threshold = State()
    waiting_for_interval = State()

@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    await message.answer("🔗 Пришли ссылку на товар:")
    await state.set_state(AddItemState.waiting_for_url)


@router.message(AddItemState.waiting_for_url)
async def process_url(message: Message, state: FSMContext):
    url = message.text.strip()

    # --- ✅ Валидация URL ---
    parsed = urlparse(url)
    if not (parsed.scheme in ("http", "https") and parsed.netloc):
        return await message.answer("❌ Это не похоже на корректную ссылку. Попробуй ещё раз.")

    await state.update_data(url=url)
    await message.answer("📉 Как ты хочешь отслеживать товар?\n\n"
                         "Напиши `цена` — если хочешь указать пороговую цену\n"
                         "Или `процент` — если хочешь отслеживать снижение на %")
    await state.set_state(AddItemState.waiting_for_type)


@router.message(AddItemState.waiting_for_type)
async def process_type(message: Message, state: FSMContext):
    choice = message.text.lower().strip()
    if choice not in ("цена", "процент"):
        return await message.answer("❌ Введи либо `цена`, либо `процент`.")

    await state.update_data(mode=choice)
    text = "Укажи пороговую цену (в рублях):" if choice == "цена" else "Укажи процент снижения (например, 15)"
    await message.answer(text)
    await state.set_state(AddItemState.waiting_for_threshold)


@router.message(AddItemState.waiting_for_threshold)
async def process_threshold(message: Message, state: FSMContext):
    user_data = await state.get_data()
    url = user_data["url"]
    mode = user_data["mode"]

    try:
        if mode == "цена":
            threshold = float(message.text.strip())
        else:
            threshold = float(message.text.strip())
            if threshold <= 0 or threshold > 100:
                raise ValueError
    except ValueError:
        return await message.answer("❌ Введи корректное число.")

    await message.answer("⏳ Получаю текущую цену товара...")

    # Запрос текущей цены с сайта
    current_price, title, _ = await fetch_price(url)

    if current_price is None:
        return await message.answer("❌ Не удалось извлечь цену. Проверь ссылку или попробуй позже.")

    await state.update_data(
        current_price=current_price,
        title=title,
        threshold=threshold
    )
    await message.answer(
        "✅ Товар распознан!\nТеперь выбери, как часто проверять цену:",
        reply_markup=interval_kb
    )
    await state.set_state(AddItemState.waiting_for_interval)

@router.message(AddItemState.waiting_for_interval)
async def process_interval(message: Message, state: FSMContext):
    interval_map = {"5 мин": 5, "15 мин": 15, "30 мин": 30, "60 мин": 60}
    interval = interval_map.get(message.text)
    if not interval:
        await message.answer("❌ Пожалуйста, выбери вариант с помощью кнопки ниже.")
        return

    user_data = await state.get_data()
    url = user_data["url"]
    mode = user_data["mode"]
    threshold = user_data["threshold"]
    current_price = user_data["current_price"]
    title = user_data["title"]

    user = await crud.get_user_by_telegram_id(message.from_user.id)
    if not user:
        user = await crud.create_user(message.from_user.id, message.from_user.username)

    await crud.add_watched_item(
        user_id=user.id,
        url=url,
        title=title,
        threshold_price=threshold if mode == "цена" else None,
        percent_change=threshold if mode == "процент" else None,
        current_price=current_price,
        check_interval=interval
    )

    await message.answer(
        f"✅ Готово! Буду следить за товаром:\n\n<b>{title or url}</b>\n"
        f"Текущая цена: {current_price} ₽\n"
        f"Интервал проверки: {interval} мин."
    )

    await state.clear()


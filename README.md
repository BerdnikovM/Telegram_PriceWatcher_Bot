# 💸 PriceWatcherBot (aiogram 3 + SQLModel + APScheduler + Playwright)

> **Telegram-бот для отслеживания цен на маркетплейсах (Wildberries, Citilink).**  
> Добавляй товары по ссылке, задавай порог или процент снижения, выбирай интервал проверки — бот сам уведомит тебя, если цена изменится.  

<p align="center">
  <img src="docs/1.png" width="720">
  <img src="docs/2.png" width="720">
  <img src="docs/3.png" width="720">
</p>

[![Docker Pulls](https://img.shields.io/docker/pulls/mihailberd/pricewatcherbot)](https://hub.docker.com/r/mihailberd/pricewatcherbot)
[![License](https://img.shields.io/github/license/BerdnikovM/Telegram_PriceWatcher_Bot)](LICENSE)

---

## ✨ Ключевые фичи

| Фича | Описание |
|------|----------|
| **Асинхронный aiogram 3** | Современная архитектура: FSM, Router, Filters |
| **Добавление товара** | /add — укажи ссылку, выбери условие и интервал |
| **Отслеживание цен** | По порогу (₽) или снижению в % |
| **Автоуведомления** | Бот присылает сообщение при изменении цены |
| **История и управление** | /list — список активных слежений, удаление кнопкой |
| **Инлайн-клавиатуры** | Удобный выбор интервала проверки |
| **База данных SQLModel** | Чистая структура: User, WatchedItem |
| **Планировщик APScheduler** | Проверка каждые N минут без блокировки бота |
| **Playwright + httpx** | Устойчивый парсинг даже при редиректах и динамике |
| **Админ-панель** | /users, /broadcast — просмотр и рассылка |

---

## 🚀 Быстрый старт

> Требования: Python 3.12+, PostgreSQL (или SQLite для локального теста), Telegram Bot API токен.

```bash
# 1. Клонируйте проект:
git clone https://github.com/GeorgePink/Telegram_PriceWatcherBot.git
cd Telegram_PriceWatcherBot

# 2. Создайте виртуальное окружение и установите зависимости:
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# 3. Создайте файл .env (см. .env.example):
BOT_TOKEN=ваш_токен
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname
ADMINS=123456789

# 4. Инициализируйте базу:
python -m app.db.init_db

# 5. Запустите бота:
python -m app.main
```

---

## 🛠️ Стек и архитектура

| Слой               | Технологии                                      |
| ------------------ | ----------------------------------------------- |
| 🐍 Язык            | **Python 3.12**                                 |
| 🤖 Telegram SDK    | **aiogram 3** (Router, FSM, Filters)            |
| 🗃️ ORM/БД         | **SQLModel** + **PostgreSQL**                   |
| ⏰ Планировщик      | **APScheduler**                                 |
| 🌐 Парсинг         | **httpx** + **BeautifulSoup4** + **Playwright** |
| 🔐 Secrets         | ENV-переменные (.env: токен, база, админы)      |
| 🧪 Тесты (roadmap) | **pytest-asyncio**, GitHub Actions CI           |
| ☁️ Деплой          | VPS/Render/Timeweb Cloud                        |

---

## 🤝 Связаться

|            | Контакт                                                                  |
| ---------- |--------------------------------------------------------------------------|
| ✉ Telegram | [@MihailBerd](https://t.me/MihailBerd)                                 |
| 💼 Kwork   | [https://kwork.ru/user/berdnikovmiha) |
| 📧 Email   | [MihailBerdWork@ya.ru](mailto:MihailBerdWork@ya.ru)                                |
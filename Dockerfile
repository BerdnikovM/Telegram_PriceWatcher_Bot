 # --- Базовый образ ---
FROM python:3.12-slim

# --- Устанавливаем системные зависимости (для playwright и psycopg2) ---
RUN apt-get update && apt-get install -y \
    curl wget gnupg build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --- Устанавливаем Playwright ---
RUN pip install playwright && playwright install --with-deps chromium

# --- Устанавливаем зависимости проекта ---
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Копируем код проекта ---
COPY . .

# --- Запуск бота ---
CMD ["python", "-m", "app.main"]


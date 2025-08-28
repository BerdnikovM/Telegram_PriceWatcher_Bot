# tests/test_parser.py

import asyncio
from app.services.parser import fetch_price


async def test_local_parser():
    url = "http://localhost:8000/product1.html"
    price, title, html = await fetch_price(url)

    print("🔍 Результаты парсинга:")
    print(f"Заголовок: {title}")
    print(f"Цена: {price}")
    print(f"HTML длина: {len(html)} символов")

    assert price is not None, "❌ Цена не найдена"
    assert price > 0, "❌ Цена некорректна"
    assert title is not None, "❌ Заголовок не найден"

    print("✅ Парсинг успешен.")


if __name__ == "__main__":
    asyncio.run(test_local_parser())


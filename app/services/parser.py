import asyncio
from decimal import Decimal, InvalidOperation
import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8"
}


async def fetch_price(url: str) -> tuple[Decimal | None, str | None, str]:
    try:
        return await try_parse_with_httpx(url)
    except Exception as e:
        print(f"[httpx] Ошибка парсинга {url}: {e}")
        print("[Fallback] Не удалось извлечь цену через httpx. Переход к Playwright...")
        return await try_parse_with_playwright(url)


# --- Быстрая попытка через httpx + BeautifulSoup
async def try_parse_with_httpx(url: str) -> tuple[Decimal | None, str | None, str]:
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    title_tag = soup.find("title")
    title = title_tag.text.strip() if title_tag else None

    # Ищем цену по маске
    import re
    price_match = re.search(r"(\d[\d\s\u00A0]{3,})\s?₽", text)
    if price_match:
        raw_price = price_match.group(1)
        price = Decimal(''.join(c for c in raw_price if c.isdigit()))
        return price, title, "httpx"
    raise ValueError("Цена не найдена через httpx")


# --- Основной метод через Playwright с улучшенной логикой
async def try_parse_with_playwright(url: str) -> tuple[Decimal | None, str | None, str]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="ru-RU")
        page = await context.new_page()

        try:
            await page.goto(url, timeout=15000)
        except Exception as e:
            print(f"[Playwright] Ошибка перехода: {e}")
            await browser.close()
            return None, None, "playwright"

        # Попробуем дождаться загрузки одного из известных блоков цен
        price_selectors = [
            "span.price-block__wallet-price",  # Wildberries
            "[data-meta-price]",              # Citilink
            "meta[itemprop='price']",         # Часто в SEO-разметке
        ]

        title_selectors = [
            "h1.product-page__title",  # WB
            "h1[color='Main']",        # Citilink
            "[data-meta-name='ProductHeaderLayout__title'] h1",
        ]

        price = None
        for selector in price_selectors:
            try:
                el = page.locator(selector).first
                await el.wait_for(timeout=5000)
                price_text = await el.text_content(timeout=3000)
                price = Decimal(''.join(c for c in price_text if c.isdigit()))
                break
            except Exception:
                continue

        title = None
        for selector in title_selectors:
            try:
                el = page.locator(selector).first
                await el.wait_for(timeout=5000)
                title = await el.text_content(timeout=3000)
                title = title.strip()
                break
            except Exception:
                continue

        await browser.close()
        return price, title, "playwright"

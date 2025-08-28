import asyncio
from app.services.parser import fetch_price


async def test_citilink():
    url = "https://www.citilink.ru/product/noutbuk-huawei-matebook-d-16-mclf-x-53013ydk-16-2024-ips-intel-core-i5-2000609/"
    price, title, _ = await fetch_price(url)
    print("\n[citilink]")
    print("Заголовок:", title)
    print("Цена:", price)


async def test_wb():
    url = "https://www.wildberries.ru/catalog/260898039/detail.aspx"
    price, title, _ = await fetch_price(url)
    print("\n[WILDBERRIES]")
    print("Заголовок:", title)
    print("Цена:", price)


if __name__ == "__main__":
    asyncio.run(test_citilink())
    # asyncio.run(test_wb())

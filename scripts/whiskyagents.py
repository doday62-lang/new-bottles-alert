import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://whiskyagents.com"
URL = BASE_URL + "/collections/neu"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}


def clean(text):
    return " ".join(text.split())


def get_products():

    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    products = []
    seen = set()

    for a in soup.select('a[href*="/products/"]'):

        href = a.get("href")
        if not href:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        seen.add(url)

        card = a
        for _ in range(8):
            if card is None:
                break

            classes = " ".join(card.get("class", [])).lower()

            if (
                "product" in classes
                or "card" in classes
                or "grid" in classes
                or "item" in classes
            ):
                break

            card = card.parent

        if card is None:
            continue

        text = clean(card.get_text(" ", strip=True))

        if len(text) < 10:
            continue

        # ---------- Цена ----------
        price = ""

        price_node = (
            card.select_one(".price")
            or card.select_one(".price-item")
            or card.select_one(".product-price")
            or card.select_one(".money")
            or card.select_one("[data-product-price]")
            or card.select_one('[class*="price"]')
        )

        if price_node:
            price = clean(price_node.get_text(" ", strip=True))

        # Если не нашли цену — ищем регулярным выражением
        if not price:
            m = re.search(r"\d+[.,]\d+\s*€", text)
            if m:
                price = m.group(0)

        # ---------- Название ----------
        name = text

        if price:
            name = text.replace(price, "").strip()

        products.append(
            {
                "id": url,
                "name": name,
                "price": price,
                "url": url,
            }
        )

    print(f"WhiskyAgents: {len(products)} товаров")

    return products

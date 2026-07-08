import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://whiskyagents.com"
URL = BASE_URL + "/ru/collections/neu"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}


def clean(text):
    return " ".join(text.split()) if text else ""


def get_products():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    products = []
    seen = set()

    # Ищем карточки товаров
    for a in soup.select('a[href*="/products/"]'):

        href = a.get("href")

        if not href:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        seen.add(url)

        name = clean(a.get_text())

        if len(name) < 5:
            continue

        # пытаемся найти цену рядом с карточкой
        price = ""

        parent = a.parent

        if parent:
            text = clean(parent.get_text())

            import re

            m = re.search(r"(\d+[.,]?\d*)\s*€", text)

            if m:
                price = m.group(0)

        products.append(
            {
                "id": url,
                "name": name,
                "price": price,
                "url": url,
            }
        )

    return products

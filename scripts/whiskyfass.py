import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://whiskyfass.de"
URL = BASE_URL + "/Neu-im-Sortiment"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}


def clean(text):
    return " ".join(text.split())


def find_price(text):
    m = re.search(r"\d+[.,]\d+\s*€", text)
    if m:
        return m.group(0)
    return ""


def get_products():

    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    selectors = [
        ".product",
        ".product-item",
        ".product-box",
        ".item",
        ".article",
        ".product--box",
        ".listing .row > div",
        ".products > *",
        ".product-grid > *",
    ]

    cards = []

    for selector in selectors:
        cards = soup.select(selector)
        if len(cards) > 5:
            print(f"Используется селектор: {selector}")
            break

    if not cards:
        cards = soup.find_all("article")

    products = []
    seen = set()

    for card in cards:

        link = card.find("a", href=True)

        if not link:
            continue

        href = link["href"]

        if (
            "konto" in href.lower()
            or "kontakt" in href.lower()
            or "newsletter" in href.lower()
            or "warenkorb" in href.lower()
        ):
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        text = clean(card.get_text(" ", strip=True))

        if len(text) < 15:
            continue

        price = find_price(text)

        name = text

        if price:
            name = name.replace(price, "").strip()

        if len(name) < 5:
            continue

        products.append(
            {
                "id": url,
                "name": name,
                "price": price,
                "url": url,
            }
        )

        seen.add(url)

    print(f"Whiskyfass: найдено {len(products)} товаров")

    return products

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

BASE_URL = "https://whiskyfass.de"
URL = BASE_URL + "/Neu-im-Sortiment"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean(text):
    return " ".join(text.split())


def get_products():

    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    products = []
    seen = set()

    # Только ссылки на товары из списка новинок
    for a in soup.select("a[href]"):

        href = a.get("href")

        if not href:
            continue

        if any(x in href.lower() for x in (
            "javascript",
            "mailto",
            "kontakt",
            "konto",
            "warenkorb",
            "newsletter",
            "#"
        )):
            continue

        # Пропускаем категории
        if href.endswith("/"):
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        card = a
        for _ in range(5):
            if card is None:
                break

            classes = " ".join(card.get("class", []))

            if any(x in classes.lower() for x in (
                "product",
                "article",
                "box",
                "item"
            )):
                break

            card = card.parent

        text = clean(card.get_text(" ", strip=True) if card else a.get_text())

        if len(text) < 15:
            continue

        price = ""

        m = re.search(r"\d+[.,]\d+\s*€", text)

        if m:
            price = m.group(0)

        name = text.replace(price, "").strip()

        products.append({
            "id": url,
            "name": name,
            "price": price,
            "url": url,
        })

        seen.add(url)

    print(f"Whiskyfass: {len(products)} товаров")

    return products

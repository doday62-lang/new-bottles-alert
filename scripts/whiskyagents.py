import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://whiskyagents.com"
URL = BASE_URL + "/collections/neu"

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

    # Ищем только ссылки на товары
    for a in soup.select('a[href*="/products/"]'):

        href = a.get("href")
        if not href:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        seen.add(url)

        # Берем только карточку товара
        card = a
        for _ in range(5):
            if card is None:
                break

            classes = " ".join(card.get("class", []))

            if any(x in classes.lower() for x in (
                "product",
                "card",
                "grid",
                "item"
            )):
                break

            card = card.parent

        text = clean(card.get_text(" ", strip=True) if card else a.get_text())

        if len(text) < 10:
            continue

        lines = [x.strip() for x in text.split() if x.strip()]

        name = text
        price = ""

        import re
        m = re.search(r"\d+[.,]?\d*\s*€", text)

        if m:
            price = m.group(0)
            name = text.replace(price, "").strip()

        products.append({
            "id": url,
            "name": name,
            "price": price,
            "url": url,
        })

    print(f"WhiskyAgents: {len(products)} товаров")

    return products

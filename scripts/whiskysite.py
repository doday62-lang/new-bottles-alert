import requests
from bs4 import BeautifulSoup

URL = "https://www.whiskysite.nl/en/collection/?sort=newest"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean(text):
    return " ".join(text.split())


def get_products():

    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    products = []
    seen = set()

    cards = soup.select("div.product-grid")

    for card in cards:

        if len(products) >= 20:
            break

        title = card.select_one("a.title")

        if title is None:
            continue

        href = title.get("href")

        if not href:
            continue

        if href in seen:
            continue

        seen.add(href)

        name = clean(title.get_text())

        price = ""

        price_node = card.select_one(
            "div.product-block-price strong"
        )

        if price_node:
            price = clean(price_node.get_text())

        products.append(
            {
                "id": href,
                "name": name,
                "price": price,
                "url": href,
            }
        )

    print(f"WhiskySite: {len(products)} товаров")

    return products

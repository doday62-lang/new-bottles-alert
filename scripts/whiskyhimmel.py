import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.whiskyhimmel.de"
URL = BASE_URL + "/schottland?page=1&sort=newest"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}


def clean(text):
    return " ".join(text.split())


def get_products():

    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=30,
        )
        response.raise_for_status()

    except requests.RequestException as e:
        print(f"WhiskyHimmel: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    products = []
    seen = set()

    cards = soup.select('a[data-hook="product-item-product-details-link"]')

    for card in cards[:40]:

        href = card.get("href")

        if not href:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        seen.add(url)

        # ---------- НАЗВАНИЕ ----------
        name = ""

        title = card.select_one('[data-hook="product-item-name"]')

        if title:
            name = clean(title.get_text(" ", strip=True))

        if not name:
            name = clean(card.get_text(" ", strip=True))

        # ---------- ЦЕНА ----------
        price = ""

        price_node = card.select_one(
            '[data-hook="product-item-price-to-pay"]'
        )

        if price_node:
            price = clean(price_node.get_text(" ", strip=True))

        products.append(
            {
                "id": url,
                "name": name,
                "price": price,
                "url": url,
            }
        )

    print(f"WhiskyHimmel: найдено {len(products)} товаров")

    return products

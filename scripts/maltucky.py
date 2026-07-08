import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://maltucky.com"
URL = BASE_URL + "/en/collections/neu"

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

    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    products = []
    seen = set()

    cards = soup.select("ul#product-grid > li.grid__item")

    for card in cards:

        if len(products) >= 20:
            break

        title = card.select_one("h3.card__heading a")

        if title is None:
            continue

        href = title.get("href")

        if not href:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        seen.add(url)

        name = clean(title.get_text(" ", strip=True))

        price = ""

        price_node = (
            card.select_one("span.price-item--regular")
            or card.select_one("span.price-item--sale")
            or card.select_one(".price-item")
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

    print(f"Maltucky: найдено {len(products)} товаров")

    return products

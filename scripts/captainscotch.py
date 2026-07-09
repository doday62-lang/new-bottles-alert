import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://captainscotch.de"
URL = BASE_URL + "/whisky-neuheiten-2/"

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

    cards = soup.select("div.product-small")

    for card in cards:

        if len(products) >= 20:
            break

        link = card.select_one("p.product-title a")

        if link is None:
            continue

        href = link.get("href")

        if not href:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        seen.add(url)

        name = clean(link.get_text(" ", strip=True))

        price = ""

        price_node = card.select_one("p.price")

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

    print(f"CaptainScotch: найдено {len(products)} товаров")

    return products

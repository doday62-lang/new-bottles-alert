import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.potstill.org"
URL = BASE_URL + "/neuheiten/"

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
        print(f"Potstill: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    products = []
    seen = set()

    cards = soup.select("div.product-box")

    for card in cards[:40]:

        link = card.select_one("a.product-name")

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

        price_node = (
            card.select_one(".product-price")
            or card.select_one(".price")
            or card.select_one(".product-price-info")
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

    print(f"Potstill: найдено {len(products)} товаров")

    return products

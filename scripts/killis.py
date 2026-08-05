import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.killis.at"
URL = BASE_URL + "/Neuheiten.html?p=1"

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
        print(f"Killis: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    products = []
    seen = set()

    cards = soup.select("div.product-item-info")

    for card in cards[:40]:

        link = card.select_one("a.product-item-link")

        if link is None:
            continue

        href = link.get("href", "").strip()

        if not href:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        seen.add(url)

        name = clean(link.get_text(" ", strip=True))

        if not name:
            name = link.get("title", "").strip()

        price = ""

        price_node = card.select_one("span.price")

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

    print(f"Killis: найдено {len(products)} товаров")

    return products

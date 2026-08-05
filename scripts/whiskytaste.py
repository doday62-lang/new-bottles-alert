import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.whiskytaste.de"
URL = BASE_URL + "/shop/?swoof=1&orderby=date"

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
        print(f"WhiskyTaste: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    products = []
    seen = set()

    cards = soup.select("li.product")

    for card in cards[:40]:

        link = card.select_one("a.woocommerce-LoopProduct-link")

        if link is None:
            continue

        url = urljoin(BASE_URL, link.get("href", ""))

        if url in seen:
            continue

        seen.add(url)

        title = card.select_one("h2.woocommerce-loop-product__title")

        if title:
            name = clean(title.get_text(" ", strip=True))
        else:
            name = clean(link.get_text(" ", strip=True))

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

    print(f"WhiskyTaste: найдено {len(products)} товаров")

    return products

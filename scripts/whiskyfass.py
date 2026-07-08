import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://whiskyfass.de/Neu-im-Sortiment"

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

    product_list = soup.select_one("#product-list")

    if product_list is None:
        print("Whiskyfass: product-list не найден")
        return []

    cards = product_list.select(
        'div.product-wrapper[itemtype*="Product"]'
    )

    products = []
    seen = set()

    for card in cards:

        link = card.select_one(
            'a.productbox-title[href]'
        )

        if link is None:
            link = card.select_one(
                'a[href]'
            )

        if link is None:
            continue

        href = link.get("href")

        if not href:
            continue

        url = urljoin(URL, href)

        if url in seen:
            continue

        seen.add(url)

        name = clean(link.get_text(" ", strip=True))

        if not name:
            continue

        price = ""

        price_node = (
            card.select_one(".price")
            or card.select_one(".product-price")
            or card.select_one(".price_wrapper")
            or card.select_one('[itemprop="price"]')
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

    products = products[:40]

    print(f"Whiskyfass: найдено {len(products)} товаров")

    return products

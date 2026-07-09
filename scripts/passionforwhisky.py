import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.passionforwhisky.com"
URL = BASE_URL + "/en/new-products/new-arrivals-whisky/"

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

    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    products = []
    seen = set()

    cards = soup.select("article.product-miniature")

    for card in cards[:40]:

        # ---------- ССЫЛКА ----------
        link = (
            card.select_one("a.product-thumbnail")
            or card.select_one("h2 a")
            or card.select_one("a[href]")
        )

        if link is None:
            continue

        url = urljoin(BASE_URL, link["href"])

        if url in seen:
            continue

        seen.add(url)

        # ---------- НАЗВАНИЕ ----------
        name = ""

        selectors = [
            ".product-title",
            "h2",
            "h3",
            ".product-name",
            ".thumbnail-title",
        ]

        for selector in selectors:

            node = card.select_one(selector)

            if node:
                text = clean(node.get_text(" ", strip=True))

                if text:
                    name = text
                    break

        # название из alt картинки
        if not name:

            img = card.select_one("img")

            if img:
                name = (
                    img.get("alt")
                    or img.get("title")
                    or ""
                ).strip()

        # название из title ссылки
        if not name:
            name = link.get("title", "").strip()

        # последнее резервное значение
        if not name:
            name = clean(link.get_text(" ", strip=True))

        # ---------- ЦЕНА ----------
        price = ""

        price_node = (
            card.select_one(".price")
            or card.select_one(".current-price")
            or card.select_one(".product-price")
            or card.select_one(".regular-price")
            or card.select_one(".price-new")
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

    print(f"PassionForWhisky: найдено {len(products)} товаров")

    return products

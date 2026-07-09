import requests
from bs4 import BeautifulSoup

URL = "https://whiskyvanzuylen.nl/whisky?orderby=nieuw&orderdirection=desc&type=Nieuwe+aanwinst"

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

    cards = soup.select("div.box-holder")

    for card in cards[:40]:

        title = card.select_one("h2")
        if not title:
            continue

        name = clean(title.get_text())

        price = ""
        price_node = card.select_one("strong.price")

        if price_node:
            price = clean(
                price_node.get_text()
                .replace("€", "€ ")
            )

        link = card.select_one("a.info")

        if not link:
            continue

        url = link.get("href", "").strip()

        if url.startswith("/"):
            url = "https://whiskyvanzuylen.nl" + url

        products.append(
            {
                "id": url,
                "name": name,
                "price": price,
                "url": url,
            }
        )

    print(f"WhiskyVanZuylen: найдено {len(products)} товаров")

    return products

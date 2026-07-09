import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.deinwhisky.de"
URL = BASE_URL + "/neues/?p=1"

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

    cards = soup.select("div.product--box.box--basic")

    for card in cards:

        title = card.select_one("a.product--title")
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

        description = ""
        desc = card.select_one("div.product--description")
        if desc:
            description = clean(desc.get_text(" ", strip=True))

        price = ""
        price_node = card.select_one("span.price--default")
        if price_node:
            price = clean(price_node.get_text(" ", strip=True))
            price = (
                price.replace("\xa0", " ")
                     .replace("*", "")
                     .strip()
            )

        if description:
            name = f"{name}\n{description}"

        products.append({
            "id": url,
            "name": name,
            "price": price,
            "url": url,
        })

    print(f"DeinWhisky: найдено {len(products)} товаров")

    return products

import requests
from bs4 import BeautifulSoup

URL = "https://utopia-spirits.at/produkt-kategorie/neu/?orderby=date&order=desc&category=neu"

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
        print(f"UtopiaSpirits: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    products = []
    seen = set()

    cards = soup.select("div.portfolio-item.product")

    for card in cards[:40]:

        title = card.select_one("div.title a")

        if title is None:
            continue

        url = title.get("href", "").strip()

        if not url:
            continue

        if url in seen:
            continue

        seen.add(url)

        name = clean(title.get_text(" ", strip=True))

        price = ""

        price_node = (
            card.select_one("div.product-price span.price")
            or card.select_one(".woocommerce-Price-amount")
            or card.select_one(".price")
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

    print(f"UtopiaSpirits: найдено {len(products)} товаров")

    return products

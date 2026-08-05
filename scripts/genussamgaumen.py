import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.genussamgaumen.at"
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

        print(f"GenussAmGaumen: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    products = []
    seen = set()

    cards = soup.select("li.product")

    for card in cards[:40]:

        try:

            link = card.select_one(
                "h4.eltdf-product-list-title a"
            )

            if not link:
                continue

            href = urljoin(
                BASE_URL,
                link.get("href"),
            )

            if href in seen:
                continue

            seen.add(href)

            title = clean(
                link.get_text(" ", strip=True)
            )

            price = ""

            price_node = card.select_one(
                "h5.eltdf-pl-price"
            )

            if price_node:
                price = clean(
                    price_node.get_text(" ", strip=True)
                )

            products.append(
                {
                    "id": href,
                    "name": title,
                    "price": price,
                    "url": href,
                }
            )

        except Exception:
            continue

    print(f"GenussAmGaumen: найдено {len(products)} товаров")

    return products


if __name__ == "__main__":

    for item in get_products():
        print(item)

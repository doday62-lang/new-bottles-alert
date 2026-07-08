import requests
from bs4 import BeautifulSoup

URL = "https://whiskyfass.de/Neu-im-Sortiment"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}


def get_products():
    """
    Возвращает список товаров.

    Формат:

    {
        "id": "...",
        "name": "...",
        "price": "...",
        "url": "..."
    }
    """

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    products = []

    links = soup.find_all("a", href=True)

    seen = set()

    for link in links:

        href = link["href"]

        if "/detail/" not in href:
            continue

        full_url = href

        if href.startswith("/"):
            full_url = "https://whiskyfass.de" + href

        if full_url in seen:
            continue

        seen.add(full_url)

        name = link.get_text(" ", strip=True)

        if len(name) < 3:
            continue

        products.append(
            {
                "id": full_url,
                "name": name,
                "price": "",
                "url": full_url,
            }
        )

    return products

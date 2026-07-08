import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://whiskyfass.de"
URL = BASE_URL + "/Neu-im-Sortiment"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean(text):
    return " ".join(text.split())


def get_products():

    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    products = []
    seen = set()

    # Берем только ссылки на реальные товары
    links = soup.select('a[href*="/detail/"]')

    if not links:
        links = soup.select('a[href*="/artikel/"]')

    if not links:
        links = soup.select('a[href*="/product/"]')

    for a in links:

        href = a.get("href")

        if not href:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        seen.add(url)

        text = clean(a.get_text(" ", strip=True))

        if len(text) < 8:
            continue

        price = ""

        m = re.search(r"\d+[.,]\d+\s*€", text)

        if m:
            price = m.group(0)
            name = text.replace(price, "").strip()
        else:
            name = text

        products.append(
            {
                "id": url,
                "name": name,
                "price": price,
                "url": url,
            }
        )

    print(f"Whiskyfass: найдено {len(products)} товаров")

    return products

import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://whiskyfass.de"
URL = BASE_URL + "/Neu-im-Sortiment"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}


def clean(text):
    if not text:
        return ""
    return " ".join(text.split())


def extract_price(text):
    m = re.search(r"(\d+[.,]\d+\s*€)", text)
    if m:
        return m.group(1)
    return ""


def get_products():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    products = []
    seen = set()

    # все ссылки на товары
    for link in soup.select("a[href]"):

        href = link.get("href")

        if not href:
            continue

        # исключаем служебные ссылки
        if any(x in href for x in (
            "/konto",
            "/warenkorb",
            "/kontakt",
            "/newsletter",
            "#",
        )):
            continue

        # ссылка должна вести на карточку товара
        if href.count("/") < 2:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        name = clean(link.get_text())

        if len(name) < 10:
            continue

        parent = link.find_parent()

        price = ""

        if parent:
            price = extract_price(parent.get_text(" ", strip=True))

        products.append({
            "id": url,
            "name": name,
            "price": price,
            "url": url,
        })

        seen.add(url)

    print(f"Whiskyfass: найдено {len(products)} товаров")

    return products

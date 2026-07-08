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


PRICE_RE = re.compile(r"\d+[.,]\d+\s*€")


def clean(text):
    return " ".join(text.split())


def find_card(node):
    """
    Поднимаемся вверх по DOM до контейнера карточки товара.
    """
    current = node

    for _ in range(8):

        if current is None:
            break

        txt = clean(current.get_text(" ", strip=True))

        # Карточка товара почти всегда содержит цену
        if PRICE_RE.search(txt):
            return current

        current = current.parent

    return None


def get_products():

    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    products = []
    seen = set()

    # Ищем только ссылки с длинным текстом
    for link in soup.find_all("a", href=True):

        href = link["href"]

        if href.startswith("#"):
            continue

        if "javascript" in href.lower():
            continue

        if any(x in href.lower() for x in (
            "konto",
            "newsletter",
            "kontakt",
            "warenkorb",
            "service",
            "blog",
            "hersteller",
        )):
            continue

        card = find_card(link)

        if card is None:
            continue

        text = clean(card.get_text(" ", strip=True))

        # Если нет цены — почти наверняка это не товар
        price_match = PRICE_RE.search(text)

        if not price_match:
            continue

        price = price_match.group(0)

        name = text.replace(price, "").strip()

        # Отбрасываем слишком короткие названия
        if len(name) < 8:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        seen.add(url)

        products.append(
            {
                "id": url,
                "name": name,
                "price": price,
                "url": url,
            }
        )

    # Удаляем возможные дубликаты по названию
    unique = {}

    for p in products:
        unique[p["name"]] = p

    products = list(unique.values())

    # Ограничиваемся первыми 40 карточками
    products = products[:40]

    print(f"Whiskyfass: найдено {len(products)} товаров")

    return products

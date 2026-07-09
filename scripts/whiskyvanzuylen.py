import requests
from bs4 import BeautifulSoup

URL = "https://whiskyvanzuylen.nl/whisky?orderby=nieuw&orderdirection=desc&type=Nieuwe+aanwinst"


def get_products():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0 Safari/537.36"
        )
    }

    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    for card in soup.select("div.product-item"):
        link = card.select_one("a")

        if not link:
            continue

        href = link.get("href")

        if href and href.startswith("/"):
            href = "https://whiskyvanzuylen.nl" + href

        title = card.select_one(".product-title")

        if title:
            title = title.get_text(" ", strip=True)
        else:
            title = link.get("title", "").strip()

        image = card.select_one("img")

        image_url = ""

        if image:
            image_url = (
                image.get("src")
                or image.get("data-src")
                or image.get("data-original")
                or ""
            )

            if image_url.startswith("/"):
                image_url = "https://whiskyvanzuylen.nl" + image_url

        if title and href:
            products.append(
                {
                    "id": href,
                    "title": title,
                    "url": href,
                    "image": image_url,
                    "shop": "Whisky Van Zuylen",
                }
            )

    return products

from playwright.sync_api import sync_playwright

URL = "https://www.dramtime.eu/product-category/whisky-en/?orderby=date"


def clean(text):
    return " ".join(text.split())


def get_products():

    products = []

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page(
                viewport={"width": 1600, "height": 1200},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0 Safari/537.36"
                ),
            )

            page.goto(
                URL,
                wait_until="networkidle",
                timeout=60000,
            )

            page.wait_for_timeout(5000)

            cards = page.locator("li.product")

            count = cards.count()

            for i in range(min(count, 40)):

                card = cards.nth(i)

                try:

                    link = card.locator("a").first.get_attribute("href")

                    if not link:
                        continue

                    title = ""

                    selectors = [
                        "h2",
                        ".woocommerce-loop-product__title",
                        ".product-title",
                        ".title",
                    ]

                    for selector in selectors:
                        loc = card.locator(selector)

                        if loc.count():
                            title = clean(loc.first.inner_text())

                            if title:
                                break

                    if not title:
                        title = clean(card.locator("a").first.inner_text())

                    price = ""

                    price_selectors = [
                        ".price",
                        ".woocommerce-Price-amount",
                        ".amount",
                    ]

                    for selector in price_selectors:
                        loc = card.locator(selector)

                        if loc.count():
                            price = clean(loc.first.inner_text())

                            if price:
                                break

                    products.append(
                        {
                            "id": link,
                            "name": title,
                            "price": price,
                            "url": link,
                        }
                    )

                except Exception:
                    continue

            browser.close()

    except Exception as e:
        print(f"Dramtime: {e}")

    print(f"Dramtime: найдено {len(products)} товаров")

    return products


if __name__ == "__main__":

    items = get_products()

    for item in items:
        print(item)

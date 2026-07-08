from storage import (
    load_products,
    save_products,
    add_product,
    is_new,
)

from telegram_sender import send_message

from whiskyagents import get_products as agents_products
from whiskyfass import get_products as fass_products


def check_store(store_name, products, known_products):

    print(f"Проверяем {store_name}...")

    new_count = 0

    for product in products:

        product_id = product["id"]

        if not is_new(product_id, known_products):
            continue

        message = (
            f"🥃 Новая бутылка!\n\n"
            f"🏪 Магазин: {store_name}\n"
            f"📦 {product['name']}\n"
        )

        if product["price"]:
            message += f"💶 {product['price']}\n"

        message += f"\n🔗 {product['url']}"

        send_message(message)

        add_product(product_id, known_products)

        new_count += 1

    print(f"{store_name}: найдено новых {new_count}")


def main():

    known_products = load_products()

    print(f"Известных товаров: {len(known_products)}")

    check_store(
        "WhiskyAgents",
        agents_products(),
        known_products,
    )

    check_store(
        "Whiskyfass",
        fass_products(),
        known_products,
    )

    save_products(known_products)

    print("Готово.")


if __name__ == "__main__":
    main()

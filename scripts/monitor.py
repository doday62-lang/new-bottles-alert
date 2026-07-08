from datetime import datetime

from storage import load_products, save_products, add_product, is_new
from telegram_sender import send_message

from whiskyagents import get_products as agents_products
from whiskyfass import get_products as fass_products
from whiskysite import get_products as whiskysite_products
from maltucky import get_products as maltucky_products


def collect_new(store_name, products, known_products):
    new_items = []

    for product in products:

        if not is_new(product["id"], known_products):
            continue

        add_product(product["id"], known_products)

        new_items.append(product)

    return {
        "store": store_name,
        "items": new_items
    }


def build_message(results):

    total = sum(len(store["items"]) for store in results)

    if total == 0:
        return None

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    lines = [
        f"🥃 Найдено {total} новых бутылок",
        f"📅 {now}",
        ""
    ]

    for result in results:

        if not result["items"]:
            continue

        lines.append("━━━━━━━━━━━━━━━━━━")
        lines.append(f"🏪 {result['store']} ({len(result['items'])})")
        lines.append("")

        for item in result["items"]:

            lines.append(f"• {item['name']}")

            if item.get("price"):
                lines.append(f"💶 {item['price']}")

            lines.append(item["url"])
            lines.append("")

    return "\n".join(lines)


def main():

    known = load_products()

    results = []

    # WhiskyAgents
    results.append(
        collect_new(
            "WhiskyAgents",
            agents_products(),
            known
        )
    )

    # Whiskyfass
    results.append(
        collect_new(
            "Whiskyfass",
            fass_products(),
            known
        )
    )

    # WhiskySite
    results.append(
        collect_new(
            "WhiskySite",
            whiskysite_products(),
            known
        )
    )

    # Maltucky
    results.append(
        collect_new(
            "Maltucky",
            maltucky_products(),
            known
        )
    )

    message = build_message(results)

    if message:
        send_message(message)
    else:
        print("Новых бутылок нет.")

    save_products(known)


if __name__ == "__main__":
    main()

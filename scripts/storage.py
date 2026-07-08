import json
from pathlib import Path

DATA_FILE = Path("data/known_products.json")


def load_products() -> set[str]:
    """
    Загружает список уже известных товаров.
    Возвращает множество строк (уникальных идентификаторов).
    """
    if not DATA_FILE.exists():
        return set()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return set(data)

        return set()

    except Exception as e:
        print(f"[storage] Ошибка чтения {DATA_FILE}: {e}")
        return set()


def save_products(products: set[str]) -> None:
    """
    Сохраняет список известных товаров.
    """

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(
            sorted(products),
            f,
            ensure_ascii=False,
            indent=2
        )


def is_new(product_id: str, known_products: set[str]) -> bool:
    """
    Проверяет, является ли товар новым.
    """
    return product_id not in known_products


def add_product(product_id: str, known_products: set[str]) -> None:
    """
    Добавляет товар в список известных.
    """
    known_products.add(product_id)

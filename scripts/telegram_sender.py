import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(text: str) -> bool:
    """
    Отправляет сообщение в Telegram.
    Возвращает True при успехе.
    """

    if not BOT_TOKEN:
        print("[telegram] BOT_TOKEN не найден")
        return False

    if not CHAT_ID:
        print("[telegram] CHAT_ID не найден")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=30,
        )

        if response.status_code == 200:
            print("[telegram] Сообщение отправлено")
            return True

        print("[telegram] Ошибка:", response.text)
        return False

    except Exception as e:
        print("[telegram] Exception:", e)
        return False

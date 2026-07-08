import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

MAX_MESSAGE_LENGTH = 3900


def _send(text: str):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": False,
        },
        timeout=30,
    )

    response.raise_for_status()


def send_message(text: str):

    if not BOT_TOKEN:
        print("BOT_TOKEN не задан")
        return

    if not CHAT_ID:
        print("CHAT_ID не задан")
        return

    if len(text) <= MAX_MESSAGE_LENGTH:
        _send(text)
        return

    parts = []
    current = ""

    for line in text.split("\n"):

        if len(current) + len(line) + 1 > MAX_MESSAGE_LENGTH:
            parts.append(current)
            current = line
        else:
            if current:
                current += "\n"
            current += line

    if current:
        parts.append(current)

    total = len(parts)

    for i, part in enumerate(parts, start=1):

        header = f"📨 Часть {i}/{total}\n\n"

        _send(header + part)

    print(f"Отправлено сообщений: {total}")

import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Делаем запас под заголовок сообщения
MAX_MESSAGE_LENGTH = 3500


def _send(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": True,
        },
        timeout=30,
    )

    if response.status_code != 200:
        print("Telegram error:")
        print(response.text)

    response.raise_for_status()


def send_message(text: str):

    if not BOT_TOKEN:
        print("BOT_TOKEN не задан")
        return

    if not CHAT_ID:
        print("CHAT_ID не задан")
        return

    # Если сообщение небольшое — отправляем сразу
    if len(text) <= MAX_MESSAGE_LENGTH:
        _send(text)
        return

    parts = []
    current = ""

    for line in text.splitlines():

        # Если одна строка слишком длинная — обрезаем её
        while len(line) > MAX_MESSAGE_LENGTH:
            parts.append(line[:MAX_MESSAGE_LENGTH])
            line = line[MAX_MESSAGE_LENGTH:]

        if not current:
            current = line
            continue

        if len(current) + len(line) + 1 > MAX_MESSAGE_LENGTH:
            parts.append(current)
            current = line
        else:
            current += "\n" + line

    if current:
        parts.append(current)

    total = len(parts)

    for i, part in enumerate(parts, start=1):
        header = f"📨 Часть {i}/{total}\n\n"
        _send(header + part)

    print(f"Отправлено сообщений: {total}")

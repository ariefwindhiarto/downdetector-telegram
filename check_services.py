# -*- coding: utf-8 -*-
import json, requests, os
from datetime import datetime

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('utf-8', errors='replace').decode('utf-8'))

with open("services.json") as f:
    urls = json.load(f)

result = []

for name, url in urls.items():
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            status = "UP"
        else:
            status = f"DOWN ({r.status_code})"
    except:
        status = "DOWN"
    result.append((name, status))

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
notif = f"📡 <b>HASIL CEK LAYANAN ({now})</b>\n\n"

for name, status in result:
    simbol = "✅" if status.startswith("UP") else "❌"
    notif += f"{simbol} <b>{name}</b> → <code>{status}</code>\n"

safe_print(notif)

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if TOKEN and CHAT_ID:
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": notif,
        "parse_mode": "HTML"
    })

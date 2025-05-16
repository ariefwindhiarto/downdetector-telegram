import json, requests, os
from datetime import datetime

with open("services.json") as f:
    urls = json.load(f)

result = []
for url in urls:
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            status = "UP"
        else:
            status = f"DOWN ({r.status_code})"
    except:
        status = "DOWN"
    result.append((url, status))

now = datetime.now().strftime("%Y-%m-%d %H:%M")
notif = f"\ud83d\udd0e <b>HASIL CEK LAYANAN ({now})</b>\n"

for u, s in result:
    simbol = "\u2705" if "UP" in s else "\u274c"
    notif += f"{simbol} {u} = <b>{s}</b>\n"

print(notif)

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if TOKEN and CHAT_ID:
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": notif,
        "parse_mode": "HTML"
    })

import json, requests, os
from datetime import datetime

# Kategorisasi manual
LOKAL = [
    "Shopee", "Tokopedia", "Bukalapak", "Lazada", "Blibli", "JD.ID",
    "TikTok", "YouTube", "Facebook", "Instagram", "WhatsApp", "Twitter (X)",
    "Telegram", "LINE", "Spotify", "Netflix", "Twitch", "Discord", "Snapchat",
    "DANA", "OVO", "GoPay", "LinkAja", "BCA", "BRI", "Mandiri", "BNI", "BTN",
    "Jenius", "SeaBank", "Telkomsel", "Indosat", "XL", "Smartfren",
    "MyRepublic", "Biznet", "First Media", "PLN", "PDAM"
]

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

# Pisahkan & sortir
def lokalitas(n): return n in LOKAL
down_services = sorted([r for r in result if "DOWN" in r[1]], key=lambda x: (not lokalitas(x[0]), x[0]))
up_services = sorted([r for r in result if "DOWN" not in r[1]], key=lambda x: (not lokalitas(x[0]), x[0]))

# Format waktu
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Format pesan
lines = [f"📢 <b>HASIL CEK LAYANAN</b> ({now})\n"]
for name, status in down_services + up_services:
    simbol = "❌" if "DOWN" in status else "✅"
    lines.append(f"{simbol} {name} → {status}")

notif = "\n".join(lines)

# Kirim ke Telegram
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if TOKEN and CHAT_ID:
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": notif,
        "parse_mode": "HTML"
    })

import requests
import os

services = {
    "Shopee": "https://shopee.co.id",
    "Biznet": "https://www.biznetnetworks.com",
    "XL": "https://xl.co.id",
    "Indosat": "https://indosatooredoo.com",
    "Telkomsel": "https://www.telkomsel.com",
    "Facebook": "https://facebook.com",
    "Instagram": "https://instagram.com",
    "TikTok": "https://tiktok.com",
    "YouTube": "https://youtube.com",
    "Tokopedia": "https://tokopedia.com",
    "WhatsApp": "https://web.whatsapp.com",
    "Google": "https://google.com"
}

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

def check_service(name, url):
    try:
        response = requests.get(url, timeout=8)
        if response.status_code >= 500:
            return f"❌ *{name}* kemungkinan *DOWN* (HTTP {response.status_code})"
    except Exception as e:
        return f"❌ *{name}* tidak dapat diakses. Error: {e}"
    return None

if __name__ == "__main__":
    messages = []
    for name, url in services.items():
        result = check_service(name, url)
        if result:
            messages.append(result)

    if messages:
        final = "🚨 *Downdetector: Layanan bermasalah!*\n\n" + "\n".join(messages)
        send_telegram(final)

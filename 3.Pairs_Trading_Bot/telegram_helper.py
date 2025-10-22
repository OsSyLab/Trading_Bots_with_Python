import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_BOT1 = os.getenv("TELEGRAM_TOKEN_BOT1")
TOKEN_BOT2 = os.getenv("TELEGRAM_TOKEN_BOT2")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(bot="bot1", message="📢 Sinyal geldi"):
    token = TOKEN_BOT1 if bot == "bot1" else TOKEN_BOT2
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"✅ Telegram mesajı ({bot}) gönderildi.")
    else:
        print(f"❌ Telegram Hatası ({bot}): {response.status_code}")
        print(response.text)

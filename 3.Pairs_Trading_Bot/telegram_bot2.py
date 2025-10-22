import os
import requests
from pair_reporter15min import analyze_bot2_signal
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN_BOT2")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Mesaj Telegram'a başarıyla gönderildi.")
    else:
        print(f"❌ Hata oluştu: {response.status_code}")
        print(response.text)

def main():
    result = analyze_bot2_signal()
    if result is not None:
        signal, score = result
        msg = f"📡 *15min/1H Sinyal Geldi!*\n\n💡 Sinyal: `{signal}`\n📊 Güven Skoru: *{score}/100*"
        send_telegram_message(msg)
    else:
        print("🔕 Sinyal yok.")

if __name__ == "__main__":
    main()

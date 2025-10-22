import pandas as pd
import os
from dotenv import load_dotenv
import requests

# === Ortam değişkenlerini yükle
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN_BOT1")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# === Veriyi yükle (DOĞRU DOSYA!)
df = pd.read_csv("bot1h_backtest_signals.csv")
df = df[df['score'] >= 90]  # 90+ skorlu sinyaller

# === En son sinyali al
if df.empty:
    print("❌ Hiç sinyal yok.")
else:
    last_signal = df.iloc[-1]
    timestamp = last_signal['timestamp']
    signal = last_signal['signal']
    score = last_signal['score']

    # RSI ve Z-score değerini almak için df_1h'yi yükle
    from pair_reporter1h import prepare_data, compute_rsi_and_sma
    df_1h = prepare_data("1h")
    df_1h['rsi'], _ = compute_rsi_and_sma(df_1h['ratio'])

    row_1h = df_1h[df_1h['timestamp'] == timestamp]
    if row_1h.empty:
        rsi_value = "?"
        zscore_value = "?"
    else:
        rsi_value = round(row_1h.iloc[0]['rsi'], 2)
        zscore_value = round(row_1h.iloc[0]['zscore'], 2)

    # === Mesaj metni
    msg = f"📉 *Yeni Sinyal (Bot1 - 1h/1d)*\n"
    msg += f"🕒 {timestamp}\n"
    msg += f"🔁 {signal}\n"
    msg += f"🎯 Skor: {score}/100\n"
    msg += f"🧠 RSI: {rsi_value} | Z-Score: {zscore_value}"

    # === Gönder
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("✅ Telegram mesajı gönderildi.")
    else:
        print("❌ Hata oluştu:", response.status_code)
        print(response.text)

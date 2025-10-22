import os
import pandas as pd
import numpy as np
from pair_reporter1h import compute_rsi_and_sma, prepare_data
from telegram_helper import send_telegram  # ✅ Telegram entegrasyonu

def backtest_bot1h():
    # === Verileri yükle ===
    df_1h = prepare_data("1h")

    # === RSI ve SMA hesapla ===
    rsi, rsi_sma = compute_rsi_and_sma(df_1h["ratio"])
    df_1h["rsi"] = rsi
    df_1h["rsi_sma"] = rsi_sma

    # === RSI kesişim sinyalleri ===
    df_1h["rsi_cross_70_up"] = (
        (df_1h["rsi"].shift(1) > df_1h["rsi_sma"].shift(1)) &
        (df_1h["rsi"] <= df_1h["rsi_sma"]) &
        (df_1h["rsi"] > 70)
    )

    df_1h["rsi_cross_30_down"] = (
        (df_1h["rsi"].shift(1) < df_1h["rsi_sma"].shift(1)) &
        (df_1h["rsi"] >= df_1h["rsi_sma"]) &
        (df_1h["rsi"] < 30)
    )

    # === 🔴 Sadece en güncel veriyi kontrol et ===
    latest = df_1h.iloc[-1]
    timestamp = latest["timestamp"]

    signal = None
    score = 0

    # --- Sinyal üretimi ---
    if (
        latest["zscore"] > 2 and
        latest["rsi_cross_70_up"] and
        latest["spread_above"]
    ):
        signal = "SELL BTC / BUY ETH"
        score = 70
    elif (
        latest["zscore"] < -2 and
        latest["rsi_cross_30_down"] and
        latest["spread_below"]
    ):
        signal = "BUY BTC / SELL ETH"
        score = 70
    else:
        print("⚪ Yeni sinyal yok.")
        return  # sinyal yoksa çık

    # --- Ek puanlar ---
    if signal.startswith("SELL"):
        if latest["zscore"] > 2.5:
            score += 10
        if latest["rsi"] > 75:
            score += 10
        if latest["spread_above"]:
            score += 10
    elif signal.startswith("BUY"):
        if latest["zscore"] < -2.5:
            score += 10
        if latest["rsi"] < 25:
            score += 10
        if latest["spread_below"]:
            score += 10

    # --- Aynı timestamp'te tekrar sinyal gönderme koruması ---
    last_file = "last_signal_bot1.txt"
    if os.path.exists(last_file):
        with open(last_file, "r") as f:
            last_sent = f.read().strip()
        if last_sent == str(timestamp):
            print(f"⏸️ {timestamp} zaten gönderilmiş, atlanıyor.")
            return

    # --- 90+ skor varsa Telegram gönder ---
    if score >= 90:
        msg = (
            f"📡 *Yeni Sinyal (Bot1 - 1h/1d)*\n"
            f"🕒 {timestamp}\n"
            f"💬 {signal}\n"
            f"🎯 Skor: {score}/100\n"
            f"🧠 RSI: {latest['rsi']:.2f} | Z-Score: {latest['zscore']:.2f}"
        )
        send_telegram(bot="bot1", message=msg)

        # timestamp'i kaydet
        with open(last_file, "w") as f:
            f.write(str(timestamp))
        print(f"✅ Yeni sinyal gönderildi ({timestamp})")
    else:
        print("⚪ Skor 90 altında, gönderilmedi.")

if __name__ == "__main__":
    backtest_bot1h()

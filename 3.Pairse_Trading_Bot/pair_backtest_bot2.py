import os
import pandas as pd
from pair_reporter15min import prepare_data, compute_rsi_and_sma
from telegram_helper import send_telegram

def detect_rsi_cross_signals(df):
    df["rsi"], df["rsi_sma"] = compute_rsi_and_sma(df["ratio"])

    df["rsi_sell_signal"] = (
        (df["rsi"].shift(1) > df["rsi_sma"].shift(1)) &
        (df["rsi"] <= df["rsi_sma"]) &
        (df["rsi"] > 70)
    )

    df["rsi_buy_signal"] = (
        (df["rsi"].shift(1) < df["rsi_sma"].shift(1)) &
        (df["rsi"] >= df["rsi_sma"]) &
        (df["rsi"] < 30)
    )

    return df

def backtest_bot2():
    # === Güncel verileri yükle ===
    df_15m = detect_rsi_cross_signals(prepare_data("15min"))
    df_1h = detect_rsi_cross_signals(prepare_data("1h"))

    # 🔎 En son (canlı) 15m verisini al
    latest_15m = df_15m.iloc[-1]
    timestamp = latest_15m['timestamp']

    # Uygun saatlik veriyi bul
    df_1h_filtered = df_1h[df_1h['timestamp'] <= timestamp]
    if df_1h_filtered.empty:
        print("⚠️ Uygun 1 saatlik veri bulunamadı.")
        return
    latest_1h = df_1h_filtered.iloc[-1]

    signal = None
    score = 0

    # === 15dk verisine göre ana sinyal üretimi ===
    if (
        latest_15m["zscore"] > 2 and
        latest_15m["rsi_sell_signal"] and
        latest_15m["spread_above"]
    ):
        signal = "SELL BTC / BUY ETH"
        score = 70
    elif (
        latest_15m["zscore"] < -2 and
        latest_15m["rsi_buy_signal"] and
        latest_15m["spread_below"]
    ):
        signal = "BUY BTC / SELL ETH"
        score = 70
    else:
        print("⚪ Sinyal yok.")
        return

    # === 1 saatlik doğrulama ===
    if signal.startswith("SELL"):
        if latest_1h["zscore"] > 2:
            score += 10
        if latest_1h["rsi"] > 70:
            score += 10
        if latest_1h["spread_above"]:
            score += 10
    elif signal.startswith("BUY"):
        if latest_1h["zscore"] < -2:
            score += 10
        if latest_1h["rsi"] < 30:
            score += 10
        if latest_1h["spread_below"]:
            score += 10

    # ✅ Eğer skor 90+ ise ve daha önce gönderilmediyse
    if score >= 90:
        last_file = "last_signal_bot2.txt"
        if os.path.exists(last_file):
            with open(last_file, "r") as f:
                last_sent = f.read().strip()
            if last_sent == str(timestamp):
                print(f"⏸️ {timestamp} zaten gönderildi, atlanıyor.")
                return

        msg = (
            f"📊 *Yeni Sinyal (Bot2 - 15m/1h)*\n"
            f"🕒 {timestamp}\n"
            f"💬 {signal}\n"
            f"🎯 Skor: {score}/100\n"
            f"📈 RSI: {latest_15m['rsi']:.2f} | Z-Score: {latest_15m['zscore']:.2f}"
        )
        send_telegram(bot="bot2", message=msg)

        with open(last_file, "w") as f:
            f.write(str(timestamp))

        print(f"✅ Yeni sinyal gönderildi ({timestamp})")
    else:
        print("⚪ Skor 90 altında, gönderilmedi.")

if __name__ == "__main__":
    backtest_bot2()

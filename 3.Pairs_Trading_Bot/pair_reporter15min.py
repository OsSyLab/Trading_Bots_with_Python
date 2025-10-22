import pandas as pd
import numpy as np
from scipy.stats import zscore
#from pair_plot import plot_pair

def compute_rsi_and_sma(series, period=14):
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    rsi_series = pd.Series(rsi, index=series.index)
    rsi_sma = rsi_series.rolling(window=period).mean()

    return rsi_series, rsi_sma

def prepare_data(timeframe):
    btc = pd.read_csv(f"btc_{timeframe}_100k.csv", parse_dates=['timestamp'])
    eth = pd.read_csv(f"eth_{timeframe}_100k.csv", parse_dates=['timestamp'])

    df = pd.merge(
        btc[['timestamp', 'close']],
        eth[['timestamp', 'close']],
        on='timestamp',
        suffixes=('_btc', '_eth')
    )

    df["ratio"] = df["close_btc"] / df["close_eth"]
    df["btc_norm"] = (df["close_btc"] - df["close_btc"].mean()) / df["close_btc"].std()
    df["eth_norm"] = (df["close_eth"] - df["close_eth"].mean()) / df["close_eth"].std()
    df["spread"] = df["btc_norm"] - df["eth_norm"]
    df["spread_ma"] = df["spread"].rolling(500).mean()
    df["spread_std"] = df["spread"].rolling(500).std()
    df["zscore"] = (df["spread"] - df["spread_ma"]) / df["spread_std"]

    # === RSI ve SMA
    rsi, rsi_sma = compute_rsi_and_sma(df["ratio"])
    df["rsi"] = rsi
    df["rsi_sma"] = rsi_sma

    # === RSI + SMA kesişim sinyalleri (TradingView mantığıyla)
    df["rsi_cross_70_up"] = (
        (df["rsi"].shift(1) > df["rsi_sma"].shift(1)) &
        (df["rsi"] <= df["rsi_sma"]) &
        (df["rsi"] > 70)
    )

    df["rsi_cross_30_down"] = (
        (df["rsi"].shift(1) < df["rsi_sma"].shift(1)) &
        (df["rsi"] >= df["rsi_sma"]) &
        (df["rsi"] < 30)
    )

    # === Diğer koşullar
    df["rsi_above_70"] = df["rsi"] > 70
    df["rsi_below_30"] = df["rsi"] < 30
    df["spread_above"] = df["spread"] > (df["spread_ma"] + 2 * df["spread_std"])
    df["spread_below"] = df["spread"] < (df["spread_ma"] - 2 * df["spread_std"])

    return df.dropna()

def analyze_bot2_signal():
    df_15m = prepare_data("15min")
    df_1h = prepare_data("1h")

    latest_15m = df_15m.iloc[-1]
    latest_1h = df_1h[df_1h['timestamp'] <= latest_15m['timestamp']].iloc[-1]

    signal = None
    score = 0

    # === 15 dakikalık temel sinyal
    if (
        latest_15m["zscore"] > 2 and
        latest_15m["rsi_cross_70_up"] and
        latest_15m["spread_above"]
    ):
        signal = "SELL BTC / BUY ETH"
        score = 70
    elif (
        latest_15m["zscore"] < -2 and
        latest_15m["rsi_cross_30_down"] and
        latest_15m["spread_below"]
    ):
        signal = "BUY BTC / SELL ETH"
        score = 70
    else:
        print("⛔ 15 dakikalıkta tüm temel koşullar sağlanmadı. Sinyal yok.")
        return None

    # === 1 saatlik sağlamalar
    if signal.startswith("SELL"):
        if latest_1h["zscore"] > 2:
            score += 10
        if latest_1h["rsi_above_70"]:
            score += 10
        if latest_1h["spread_above"]:
            score += 10
    elif signal.startswith("BUY"):
        if latest_1h["zscore"] < -2:
            score += 10
        if latest_1h["rsi_below_30"]:
            score += 10
        if latest_1h["spread_below"]:
            score += 10

    # === Sonuç
    print(f"\n✅ Sinyal: {signal}")
    print(f"📊 Güven Skoru: {score}/100")
    print(f"🕒 Tarih: {latest_15m['timestamp']}")
    #plot_pair(df_15m)

    return signal, score

if __name__ == "__main__":
    analyze_bot2_signal()

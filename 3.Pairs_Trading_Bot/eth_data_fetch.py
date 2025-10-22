from binance.client import Client
import pandas as pd
import datetime as dt
import time

# === Binance API Anahtarlarını gir ===
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

client = Client(api_key, api_secret)

# === 1 günlük mumları indirmek için ayarlar ===
symbol = "ETHUSDT"
interval = Client.KLINE_INTERVAL_1DAY   # <-- 1 günlük periyot
total_bars = 100000
limit = 1000
filename = "eth_1d_100k.csv"

# === Başlangıç tarihi ===
start_date = dt.datetime(2015, 8, 1)  # ETH'in geçmişi için uygun başlangıç
data = []

print(f"📊 {symbol} için 1 günlük veri çekme işlemi başladı...")

# === Veri çekme döngüsü ===
while len(data) < total_bars:
    start_str = start_date.strftime("%d %b %Y %H:%M:%S")
    klines = client.get_historical_klines(symbol, interval, start_str)

    if not klines:
        print("✅ Veri çekme tamamlandı veya daha fazla veri bulunamadı.")
        break

    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])

    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    data.append(df)
    last_time = df['timestamp'].iloc[-1]
    start_date = last_time + dt.timedelta(days=1)

    print(f"✅ {len(df)} bar eklendi, toplam: {len(pd.concat(data))}")

    time.sleep(0.5)

# === Veriyi birleştir ve kaydet ===
full_df = pd.concat(data)
full_df = full_df.drop_duplicates(subset='timestamp')
full_df = full_df.set_index('timestamp')
full_df.to_csv(filename)

print(f"\n✅ Veri çekme tamamlandı: {len(full_df)} satır kaydedildi -> {filename}")

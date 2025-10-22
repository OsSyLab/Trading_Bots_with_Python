import time
import datetime as dt
import pandas as pd
from binance.client import Client

# 🔐 Binance API Anahtarları
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
client = Client(api_key, api_secret)

# 🎯 Parametreler
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1DAY  # 🔄 Günlük (1d)
total_bars = 100000
filename = "btc_1d_100k.csv"

# 📅 Başlangıç tarihi
start_date = dt.datetime(year=2015, month=1, day=1)  # Günlük veriler için daha geriden başlanabilir
data = []

print(f"📥 {symbol} için 1 günlük veri çekme işlemi başladı...")

while len(data) < total_bars:
    start_str = start_date.strftime("%d %b %Y %H:%M:%S")
    klines = client.get_historical_klines(symbol, interval, start_str)

    if not klines:
        print("✅ Veri çekme tamamlandı veya daha fazla veri yok.")
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
    time.sleep(0.5)

# 🔄 Tüm verileri birleştir
result = pd.concat(data)

# 💾 CSV olarak kaydet
print(f"✅ {symbol} için veri çekme tamamlandı: {len(result)} satır -> {filename}")
result.to_csv(filename, index=False)

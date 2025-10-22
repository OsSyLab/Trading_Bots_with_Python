import pandas as pd
import time
import datetime
from binance.client import Client

# Binance API Kimliğiniz - eğer varsa
api_key = ''
api_secret = ''

# Binance istemcisini başlat
client = Client(api_key, api_secret)

# Parametreler
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_5MINUTE
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime(2025, 10, 19)
delta = datetime.timedelta(days=30)

# Tüm verileri burada biriktireceğiz
all_klines = []

# Başlangıç zamanından bitiş zamanına kadar döngü
current = start_date
while current < end_date:
    next_date = current + delta

    print(f"Veri çekiliyor: {current.strftime('%Y-%m-%d')} -> {next_date.strftime('%Y-%m-%d')}")
    klines = client.get_historical_klines(
        symbol,
        interval,
        current.strftime("%Y-%m-%d %H:%M:%S"),
        next_date.strftime("%Y-%m-%d %H:%M:%S")
    )

    all_klines.extend(klines)
    print(f"Toplam veri: {len(all_klines)} satır")

    current = next_date
    time.sleep(1)  # Rate limit'e takılmamak için

    # Eğer 250.000'den fazla veriye ulaşıldıysa durdur
    if len(all_klines) >= 250_000:
        print("250.000 veri alındı, durduruluyor.")
        break

# DataFrame'e çevir
df = pd.DataFrame(
    all_klines,
    columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ]
)

# Sadece gerekli sütunları al ve sayısal yap
df = df[["open", "high", "low", "close", "volume"]].astype(float)

# CSV'ye kaydet
df.to_csv("btc_5min_250k.csv", index=False)
print("✅ Veri kaydedildi: btc_5min_250k.csv")
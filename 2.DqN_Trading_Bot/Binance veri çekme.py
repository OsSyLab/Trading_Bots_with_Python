import pandas as pd
import time
from datetime import datetime, timedelta
from binance.client import Client

# 🔑 API bilgileri (test/gerçek)
api_key = ''
api_secret = ''
client = Client(api_key, api_secret)

# 📊 Parametreler
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_5MINUTE
now = datetime.now()

# 5 dakikalık veri → günde 288 satır → 300000 / 288 ≈ 1045 gün
days_required = int(300_000 / 288) + 5
start_date = now - timedelta(days=days_required)
end_date = now

print(f"📅 Hedef aralık: {start_date.strftime('%Y-%m-%d')} → {end_date.strftime('%Y-%m-%d')}")

# Veri çekim döngüsü
all_klines = []
delta = timedelta(days=30)
current = start_date

while current < end_date:
    next_date = current + delta
    print(f"\n⏳ Veri çekiliyor: {current.date()} → {next_date.date()}")

    try:
        klines = client.get_historical_klines(
            symbol,
            interval,
            current.strftime("%Y-%m-%d %H:%M:%S"),
            next_date.strftime("%Y-%m-%d %H:%M:%S")
        )

        if not klines:
            print("⚠️ Yeni veri gelmedi, devam ediliyor...")
        else:
            all_klines.extend(klines)
            print(f"📈 Toplam veri: {len(all_klines)} satır")

        # 300.000 sınırına ulaştıysak durdur
        if len(all_klines) >= 300_000:
            print("✅ 300.000 veri sınırına ulaşıldı.")
            break

    except Exception as e:
        print(f"❌ Hata: {e}")
        time.sleep(2)

    current = next_date
    time.sleep(0.5)

# 🧩 DataFrame’e çevir
df = pd.DataFrame(all_klines, columns=[
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
])

# 🧹 Temizle ve sadeleştir
df = df[["open_time", "open", "high", "low", "close", "volume"]].copy()
df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

# 💾 CSV’ye kaydet
output_file = "btc_5min_300k.csv"
df.to_csv(output_file, index=False)

print("\n✅ Kayıt tamamlandı:", output_file)
print(f"📊 Veri aralığı: {df['open_time'].iloc[0]} → {df['open_time'].iloc[-1]}")
print(f"🧮 Toplam satır: {len(df)}")


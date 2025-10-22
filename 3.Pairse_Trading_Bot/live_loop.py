import time
from pair_backtest_bot1 import backtest_bot1h
from pair_backtest_bot2 import backtest_bot2

while True:
    print("\n🔄 Yeni tarama başlatıldı...\n")

    try:
        backtest_bot1h()
        backtest_bot2()
    except Exception as e:
        print(f"❌ Hata: {e}")

    print("\n⏳ 15 dakika bekleniyor...\n")
    time.sleep(15 * 60)  # 15 dakika bekle

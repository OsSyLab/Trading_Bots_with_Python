import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import DQN
from env_trading import ThreeCandleEnv

# Ortamı başlat
env = ThreeCandleEnv("btc_test.csv")
model = DQN.load("dqn_trading_model")

# Başlangıç parametreleri
balance = 10_000.0
position = 0.0
entry_price = 0.0
COMMISSION_RATE = 0.00075
total_commission_paid = 0.0

# İzleme listeleri
portfolio_value = [balance]
real_buys = []
real_sells = []
trades = []

# Sayaçlar
buy_count = 0
sell_count = 0

# Ortamı sıfırla
obs = env.reset()
done = False

while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)

    if env.current_step >= len(env.df):
        break

    price = env.df.iloc[env.current_step]["close"]

    # AL
    if action == 1 and position == 0:
        quantity = (balance * (1 - COMMISSION_RATE)) / price
        commission = balance * COMMISSION_RATE
        total_commission_paid += commission

        entry_price = price
        position = quantity
        balance = 0.0
        real_buys.append(env.current_step)
        buy_count += 1

    # SAT
    elif action == 2 and position > 0:
        proceeds = (position * price) * (1 - COMMISSION_RATE)
        commission = (position * price) * COMMISSION_RATE
        total_commission_paid += commission

        balance = proceeds
        trades.append((entry_price, price))
        position = 0.0
        entry_price = 0.0
        real_sells.append(env.current_step)
        sell_count += 1

    current_value = position * price if position > 0 else balance
    portfolio_value.append(current_value)

# Eğer pozisyon açık kaldıysa değerini dikkate al
if position > 0:
    final_price = env.df.iloc[-1]["close"]
    unrealized_value = position * final_price
    portfolio_value[-1] = unrealized_value
    print(f"⚠️ Son pozisyon kapanmadı. Gerçekleşmemiş değer: ${unrealized_value:.2f}")

# --- GRAFİKLER ---
plt.figure(figsize=(14, 8))

# 1️⃣ AL/SAT noktaları
plt.subplot(2, 1, 1)
plt.plot(env.df['close'].values[:len(portfolio_value)], label="Fiyat", color="steelblue", alpha=0.7)
plt.scatter(real_buys, env.df['close'].values[real_buys], marker="^", color="green", s=80, label="AL")
plt.scatter(real_sells, env.df['close'].values[real_sells], marker="v", color="red", s=80, label="SAT")
plt.title("AL / SAT Noktaları")
plt.legend()
plt.grid(True)

# 2️⃣ Portföy değeri
plt.subplot(2, 1, 2)
plt.plot(portfolio_value, label="Portföy Değeri", color="blue")
plt.title("Getiri Eğrisi")
plt.xlabel("Adım")
plt.ylabel("USD")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# --- PERFORMANS ÖZETİ ---
total_trades = len(trades)
profitable = sum(1 for buy, sell in trades if sell > buy)
losses = total_trades - profitable

avg_profit = (
    np.mean([
        ((sell * (1 - COMMISSION_RATE)) - (buy * (1 + COMMISSION_RATE))) /
        (buy * (1 + COMMISSION_RATE)) * 100
        for buy, sell in trades
    ]) if trades else 0.0
)

print("\n📊 --- Trade Özeti ---")
print(f"Toplam işlem sayısı: {total_trades}")
print(f"✅ Karlı işlemler: {profitable}")
print(f"❌ Zararlı işlemler: {losses}")
if total_trades > 0:
    print(f"📈 Başarı oranı: {profitable / total_trades * 100:.2f}%")
print(f"💵 Ortalama işlem başı getiri: %{avg_profit:.2f}")
print(f"🔻 Toplam komisyon maliyeti: ${total_commission_paid:.2f}")
print(f"💰 Son Portföy Değeri: ${portfolio_value[-1]:.2f}")
print(f"📌 Son adımda pozisyon var mı? {'✅ Evet' if position > 0 else '❌ Hayır'}")
print(f"🔁 Toplam ALIM sayısı: {buy_count}, SATIM sayısı: {sell_count}")

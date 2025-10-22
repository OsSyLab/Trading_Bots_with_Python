import os
import gym
import numpy as np
from tqdm import tqdm  # 👈 İlerleme çubuğu
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from env_trading import ThreeCandleEnv

# Ortamı başlat
env = DummyVecEnv([lambda: ThreeCandleEnv("btc_train.csv")])

# Modeli oluştur
model = DQN(
    policy="MlpPolicy",
    env=env,
    learning_rate=1e-4,
    buffer_size=50_000,
    learning_starts=1_000,
    batch_size=64,
    tau=1.0,
    gamma=0.99,
    train_freq=1,
    target_update_interval=500,
    exploration_fraction=0.1,
    exploration_final_eps=0.01,
    verbose=0,  # tqdm ile daha sade görünüm için kapatıyoruz
)

# Eğitim adımı
TOTAL_STEPS = 200_000
STEP_CHUNK = 10_000

# 👇 tqdm ile adım adım takip
print(f"🚀 Eğitim başlatılıyor: {TOTAL_STEPS} adım")
for i in tqdm(range(0, TOTAL_STEPS, STEP_CHUNK), desc="📈 Eğitim İlerlemesi"):
    model.learn(total_timesteps=STEP_CHUNK, reset_num_timesteps=False, progress_bar=False)

# Modeli kaydet
model.save("dqn_trading_model")
print("✅ Model kaydedildi: dqn_trading_model.zip")

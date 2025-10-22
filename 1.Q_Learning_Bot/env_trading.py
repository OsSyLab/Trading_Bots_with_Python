import numpy as np
import pandas as pd
import gymnasium as gym
from gymnasium import spaces

class ThreeCandleEnv(gym.Env):
    def __init__(self, csv_file_path):
        super(ThreeCandleEnv, self).__init__()

        # Veriyi yükle
        self.df = pd.read_csv(csv_file_path)
        self.df.dropna(inplace=True)

        self.current_step = 3  # En az 3 mumdan başlamalıyız
        self.done = False

        # Gözlem uzayı: son 3 mumun open-high-low-close-volume değerleri (3x5=15 özellik)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(15,), dtype=np.float32)

        # Aksiyon uzayı: 0 = Bekle, 1 = Al, 2 = Sat
        self.action_space = spaces.Discrete(3)

        self.position = 0  # 0: pozisyon yok, 1: long pozisyon

        self.buy_price = 0
        self.total_profit = 0

    def reset(self):
        self.current_step = 3
        self.position = 0
        self.buy_price = 0
        self.total_profit = 0
        self.done = False
        return self._get_observation()

    def _get_observation(self):
        # Son 3 mumun verilerini düzleştir (flatten)
        window = self.df.iloc[self.current_step - 3:self.current_step][["open", "high", "low", "close", "volume"]]
        obs = window.values.flatten()
        return obs.astype(np.float32)

    def step(self, action):
        reward = 0

        current_price = self.df.iloc[self.current_step]["close"]

        # Aksiyon işle
        if action == 1:  # Al
            if self.position == 0:
                self.position = 1
                self.buy_price = current_price
        elif action == 2:  # Sat
            if self.position == 1:
                reward = current_price - self.buy_price
                self.total_profit += reward
                self.position = 0

        self.current_step += 1
        if self.current_step >= len(self.df):
            self.done = True

        return self._get_observation(), reward, self.done, {}

    def render(self, mode="human"):
        print(f"Step: {self.current_step}, Total Profit: {self.total_profit:.2f}")
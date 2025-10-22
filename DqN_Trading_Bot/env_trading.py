import numpy as np
import pandas as pd
import gym
from gym import spaces


class ThreeCandleEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, csv_file_path):
        super(ThreeCandleEnv, self).__init__()

        # --- VERİ YÜKLE ---
        self.df = pd.read_csv(csv_file_path)
        self.df.dropna(inplace=True)

        # --- EMA21 ---
        self.df["EMA21"] = self.df["close"].ewm(span=21, adjust=False).mean()

        # --- ATR ve MOST ---
        self.df["ATR"] = (self.df["high"] - self.df["low"]).rolling(window=14).mean()
        self.df["MOST"] = self.df["EMA21"] - 3 * self.df["ATR"]

        # --- RSI ---
        delta = self.df["close"].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(window=14).mean()
        avg_loss = pd.Series(loss).rolling(window=14).mean()
        rs = avg_gain / avg_loss
        self.df["RSI"] = 100 - (100 / (1 + rs))

        # --- MACD ---
        ema12 = self.df["close"].ewm(span=12, adjust=False).mean()
        ema26 = self.df["close"].ewm(span=26, adjust=False).mean()
        self.df["MACD"] = ema12 - ema26
        self.df["MACD_signal"] = self.df["MACD"].ewm(span=9, adjust=False).mean()

        # --- OBV (On-Balance Volume) ---
        self.df["OBV"] = (np.sign(self.df["close"].diff()) * self.df["volume"]).fillna(0).cumsum()

        self.df.dropna(inplace=True)

        # --- BAŞLANGIÇ DURUMLARI ---
        self.current_step = 30  # Göstergelerin hesaplanması için güvenli başlangıç
        self.initial_balance = 10_000
        self.balance = self.initial_balance
        self.position = 0
        self.entry_price = 0
        self.total_profit = 0
        self.done = False
        self.commission_rate = 0.0015

        # --- OBSERVATION SPACE (Dinamik) ---
        sample_obs = self._get_observation()
        obs_dim = sample_obs.shape[0]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(obs_dim,), dtype=np.float32)

        # --- ACTION SPACE ---
        self.action_space = spaces.Discrete(3)  # 0: Bekle, 1: Al, 2: Sat

    # --- GÖZLEM HAZIRLA ---
    def _get_observation(self):
        if self.current_step >= len(self.df):
            return np.zeros(1, dtype=np.float32)

        window = self.df.iloc[self.current_step - 3:self.current_step]

        # 3 mumluk OHLC + 3 hacim + MOST + RSI + MACD + EMA21 + OBV
        candles = window[["open", "high", "low", "close"]].values.flatten()
        volumes = window["volume"].values
        row = self.df.iloc[self.current_step]

        indicators = np.array([
            row["MOST"],
            row["RSI"],
            row["MACD"],
            row["MACD_signal"],
            row["EMA21"],
            row["OBV"]
        ])

        obs = np.concatenate((candles, volumes, indicators))
        return obs.astype(np.float32)

    # --- RESET ---
    def reset(self):
        self.current_step = 30
        self.balance = self.initial_balance
        self.position = 0
        self.entry_price = 0
        self.total_profit = 0
        self.done = False
        return self._get_observation()

    # --- STEP ---
    def step(self, action):
        if self.done or self.current_step >= len(self.df):
            self.done = True
            return self._get_observation(), 0, self.done, {}

        current_price = self.df.iloc[self.current_step]["close"]
        reward = 0

        # --- AL ---
        if action == 1 and self.position == 0:
            quantity = self.balance / current_price
            cost = quantity * current_price
            commission = cost * self.commission_rate

            self.position = quantity
            self.entry_price = current_price
            self.balance -= (cost + commission)
            reward -= commission * 2  # Komisyon bilinci

        # --- SAT ---
        elif action == 2 and self.position > 0:
            proceeds = self.position * current_price
            commission = proceeds * self.commission_rate
            profit = proceeds - (self.entry_price * self.position)

            self.balance += proceeds - commission
            self.total_profit += profit
            self.position = 0
            self.entry_price = 0

            reward = 1 if profit > 0 else -1
            if profit < 0:
                reward -= commission * 2  # Zararda ekstra ceza

        # --- HATALI İŞLEM CEZASI ---
        if (action == 1 and self.position > 0) or (action == 2 and self.position == 0):
            reward -= 0.1

        # --- BEKLEMEYE KÜÇÜK CEZA ---
        if action == 0:
            reward -= 0.01

        # --- ADIM GÜNCELLE ---
        self.current_step += 1
        if self.current_step >= len(self.df):
            self.done = True

        return self._get_observation(), reward, self.done, {}

    # --- GÖRSEL ÇIKTI ---
    def render(self, mode="human"):
        print(
            f"Step: {self.current_step} | Balance: ${self.balance:.2f} | "
            f"Position: {self.position:.6f} BTC | Total Profit: ${self.total_profit:.2f}"
        )

# 🧠 Q-Learning Trading Bot

This folder contains an implementation of a **Q-Learning-based trading bot** in Python.  
It uses historical BTC price data and trains a reinforcement learning agent to make buy/sell/hold decisions.

---

## 📌 Overview

- **Model**: Q-Learning (tabular)
- **Environment**: Custom trading environment based on historical OHLC data
- **Data**: BTC/USDT 5-minute candle data (CSV)
- **Goal**: Learn an optimal policy for maximizing cumulative profit over time

---

## 🧠 File Descriptions

| File | Description |
|------|-------------|
| `btc_5min_250k.csv` | Historical BTC/USDT price data (5-minute candles, ~250,000 rows). |
| `Binance veri çekme.py` | (Optional) Script to fetch fresh data from Binance and update the dataset. |
| `env_trading.py` | Defines the custom **Trading Environment** (state space, rewards, terminal conditions). |
| `q_learning_agent.py` | Implements the **Q-Learning Agent** (Q-table, epsilon-greedy policy, update logic). |
| `train_q_agent.py` | Trains the agent in the trading environment for a number of episodes. |
| `test_env.py` | Tests and validates the environment separately before training. |
| `Verilerin Kontrolu.py` | Helper script for inspecting and verifying data before use. |

---

## 🚀 How It Works

### 1. Environment

The environment (`env_trading.py`) simulates a trading scenario where:

- **States**: consist of indicators like price, position, returns, etc.
- **Actions**: are `Buy`, `Sell`, or `Hold`
- **Rewards**: are based on profit/loss after each action

### 2. Agent

- The agent uses a **Q-table** to map `(state, action)` pairs to expected rewards.
- It chooses actions via an **epsilon-greedy** exploration strategy.
- Updates its policy with the **Bellman equation** after each step.

---

## 📊 Training

Run:


python train_q_agent.py

Loads the CSV

Initializes environment and agent

Trains over multiple episodes

Prints logs of total profit per episode

📈 Backtesting & Evaluation

After training, you can visualize or log:

Episode reward/profit

Win rate (% of profitable trades)

Q-table values

🔧 Optional Improvements

Use Deep Q-Learning (DQN) instead of a Q-table for larger state spaces.

Add technical indicators (RSI, MACD, etc.) to the state.

Normalize and clean data in preprocessing.

📢 Notes

.csv file should be cleaned and normalized before training.

Actions are applied sequentially, one step per candle.

The bot assumes no trading fees/slippage in this basic version.

📬 Contact

📱 Follow me on X (Twitter): @OsSy_Lab
                                            https://x.com/OsSy_Lab                

💬 DMs are open for collaboration or questions!

License

**MIT License**  
You are free to use, modify, and distribute this code with attribution.  

© 2025 **Data Solutions Lab. by Osman Uluhan** – All rights reserved.

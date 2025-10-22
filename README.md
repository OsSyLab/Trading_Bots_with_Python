<p align="center">
https://github.com/OsSyLab/Trading_Bots_with_Python/blob/4911351195c3a3d723f239680513b0a13bc26b0b/GITHUB%20Bannerlar%20(2).png
</p>



# 🤖 Trading_Bots_with_Python

A collection of automated trading bots built with Python.  
Includes different strategies for algorithmic trading, such as:

---

## 🧠 Contents

### 1. **DQN Trade Bot**
- Strategy: Deep Q-Network with neural networks
- Uses: Keras/Tensorflow for decision making
- File: `dqn-crypto-trading-bot`

### 2. **Q-Learning Trade Bot**
- Strategy: Reinforcement Learning (Q-Learning)
- Goal: Learn to trade based on reward/punishment system.
- File: `btc-qlearning-tradebot`


### 3. **Pairs Trading Bot**
- Strategy: Statistical arbitrage using Z-Score & RSI.
- Timeframes: 15m/1h (Bot2), 1h/1d (Bot1)
- Notifications: Telegram alerts on high-confidence signals
- Files:
  - `pair_backtest_bot1.py`
  - `pair_backtest_bot2.py`
  - `pair_reporter1h.py`, `pair_reporter15min.py`
  - `telegram_helper.py`

---

## ⚙️ Installation


git clone https://github.com/OsSyLab/Trading_Bots_with_Python.git
cd Trading_Bots_with_Python
pip install -r requirements.txt
🚀 Usage
Configure .env for Telegram API keys if using signals

Run bots manually or use a scheduler / deployment (e.g. Render.com)

📬 Telegram Alerts
To receive real-time trading signals, configure:

TELEGRAM_TOKEN_BOT1

TELEGRAM_TOKEN_BOT2

TELEGRAM_CHAT_ID

📈 Disclaimer
This project is for educational purposes only.
Not financial advice. Trade at your own risk.

📬 Contact

📱 Follow me on X (Twitter): @OsSy_Lab
                https://x.com/OsSy_Lab        

**MIT License**  
You are free to use, modify, and distribute this code with attribution.  

© 2025 **Data Solutions Lab. by Osman Uluhan** – All rights reserved.

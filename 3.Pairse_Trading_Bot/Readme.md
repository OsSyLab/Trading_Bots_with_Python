# 🤖 Pairs Trading Bot

This directory contains a fully automated **Pairs Trading Bot** developed in Python.  
The bot monitors the BTC/ETH ratio and sends **Telegram alerts** when statistically significant signals occur.

---

## 📌 Overview

- **Strategy**: Statistical arbitrage based on **Z-Score**, **RSI**, and **Spread** metrics.
- **Timeframes**:
  - Bot1: 1H & 1D
  - Bot2: 15min & 1H confirmation
- **Alert System**: Telegram messages for signals with high confidence score (90+).
- **Live mode**: Scans every 15 minutes continuously.

---

## 🧠 File Structure & Purpose

| File | Description |
|------|-------------|
| `btc_data_fetch.py` | Fetches BTC historical price data from CSV (or other sources). |
| `eth_data_fetch.py` | Fetches ETH historical price data from CSV (or other sources). |
| `pair_reporter1h.py` | Computes **RSI**, **SMA**, and data prep for 1-hour timeframe. |
| `pair_reporter15min.py` | Same as above but for 15-minute resolution. |
| `pair_backtest_bot1.py` | Backtest logic for **Bot1** (1H/1D), based on RSI & Z-Score crossover. |
| `pair_backtest_bot2.py` | Backtest logic for **Bot2** (15m live signal with 1H confirmation). |
| `telegram_helper.py` | Generic helper to send messages via Telegram bots. |
| `telegram_bot1.py` | Used for real-time messaging for **Bot1** signals. |
| `telegram_bot2.py` | Used for real-time messaging for **Bot2** signals. |
| `live_loop.py` | Live-mode loop script — executes bots every 15 minutes. |
| `.env.example` | Example file for storing your bot tokens and secrets (edit to `.env`). |

---

## ⚙️ How It Works

### 🔁 Backtest Flow (Bot1 & Bot2)

1. Loads and merges BTC/ETH data.
2. Computes:
   - Price **ratio**
   - **RSI** and its **SMA**
   - **Z-score** for mean reversion
   - Spread condition (above/below threshold)
3. Checks signal rules and assigns confidence **score (0–100)**.
4. If score ≥ 90 → sends Telegram alert and logs it.
5. Saves signals to CSV and plots relevant ones.

---

## 🚀 Live Execution

The `live_loop.py` script is used to run both bots in production:


python live_loop.py

Scans every 15 minutes.

Skips historical signals — only acts on the most recent candle.

Sends alert to Telegram if a valid signal is found.

📦 Environment Setup

Clone repo:

git clone https://github.com/OsSyLab/Trading_Bots_with_Python.git


Install requirements (if any):

pip install -r requirements.txt


Setup .env:
Rename .env.example → .env and set your Telegram bot token & chat ID.

🧪 Example Signal
📡 New Signal (Bot1 - 1H/1D)
🕒 2025-10-22 12:00:00
💬 SELL BTC / BUY ETH
🎯 Score: 90/100
🧠 RSI: 74.32 | Z-Score: 2.61

📊 Output Files

bot1h_backtest_signals.csv

bot2_backtest_signals.csv

These CSVs store all signal timestamps, direction, and confidence scores.

📈 Visualization

When signals reach 90+, a matplotlib plot is automatically generated showing entry points on the BTC/ETH ratio graph.

🔐 Security Note

Make sure .env file is excluded from commits (via .gitignore) and never shared publicly.

📬 Contact

📱 Follow me on X (Twitter): @OsSy_Lab
                                            https://x.com/OsSy_Lab      

License

**MIT License**  
You are free to use, modify, and distribute this code with attribution.  

© 2025 **Data Solutions Lab. by Osman Uluhan** – All rights reserved.

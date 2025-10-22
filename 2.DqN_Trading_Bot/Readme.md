# 🧠 DQN Crypto Trading Bot

A Deep Q-Network (DQN) based crypto trading bot built using Python and Binance 5-minute candlestick data.

This project is an experimental implementation of reinforcement learning in financial markets using a custom OpenAI Gym environment.

---

## 📁 Project Structure

- `Binance veri çekme.py`  
  → Downloads 5-minute historical candlestick data from Binance API.

- `btc_5min_300k.csv`  
  → Cleaned dataset of 300,000 rows used for training and testing.

- `env_trading.py`  
  → Custom `gym.Env` that defines the trading logic, reward shaping, and environment behavior.

- `train_dqn.py`  
  → Implements training loop for a Deep Q-Network agent.

- `test_dqn.py`  
  → Tests the trained model on unseen data and prints performance metrics.

---

## 🚀 How to Run

> ⚠️ Make sure you have Python 3.8+ and dependencies installed.

```bash
# Install dependencies (adjust as needed)
pip install numpy pandas gym tensorflow keras matplotlib

# (Optional) Pull fresh data
python "Binance veri çekme.py"

# Train the model
python train_dqn.py

# Test the model
python test_dqn.py
🎯 Next Steps
This project is still in early experimental phase. Planned improvements include:

Reward function tuning

More advanced indicators

Pair trading strategies (e.g., BTC-ETH Z-score arbitrage)

Integration with live trading APIs (Binance Spot Testnet)

📌 Disclaimer
This project is for research and educational purposes only.
Not financial advice. Use at your own risk.

📬 Contact

📱 Follow me on X (Twitter): @OsSy_Lab
                                            https://x.com/OsSy_Lab                

💬 DMs are open for collaboration or questions!

License

**MIT License**  
You are free to use, modify, and distribute this code with attribution.  

© 2025 **Data Solutions Lab. by Osman Uluhan** – All rights reserved.
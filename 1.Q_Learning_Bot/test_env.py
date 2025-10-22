from env_trading import ThreeCandleEnv

env = ThreeCandleEnv("btc_5min_250k.csv")

obs = env.reset()
print("İlk gözlem:", obs)

done = False
total_reward = 0

while not done:
    action = env.action_space.sample()  # Rastgele aksiyon seç (şimdilik)
    obs, reward, done, _ = env.step(action)
    total_reward += reward

    if reward != 0:
        print(f"Aksiyon: {action}, Ödül: {reward:.2f}, Toplam Kâr: {total_reward:.2f}")

env.render()
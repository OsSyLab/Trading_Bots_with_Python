from env_trading import ThreeCandleEnv
from q_learning_agent import QLearningAgent

env = ThreeCandleEnv("btc_5min_250k.csv")
def obs_to_state(obs):
    return hash(tuple(obs)) % 100000
state_size = 100000
action_size = env.action_space.n

agent = QLearningAgent(state_size, action_size)

num_episodes = 100  # Daha yüksek sayılar daha iyi öğrenme sağlar

for episode in range(num_episodes):
    obs = env.reset()
    state = obs_to_state(obs)
    done = False
    total_reward = 0

    while not done:
        action = agent.act(state)
        obs, reward, done, _ = env.step(action)
        next_state = obs_to_state(obs)
        agent.learn(state, action, reward, next_state)
        state = next_state
        total_reward += reward

    agent.decay_epsilon()

    print(f"Episode {episode + 1}/{num_episodes} - Toplam Kâr: {total_reward:.2f} - Epsilon: {agent.epsilon:.4f}")

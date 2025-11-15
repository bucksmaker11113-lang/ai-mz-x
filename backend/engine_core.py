# engine_core.py
# MZ/X AI Trading Engine – Éles Q-learning alapu döntési motor

import numpy as np
import time
import settings
from market_stream_manager import MarketStreamManager
from ai_qlearning import QLearningAgent

class TradingEngine:
    def __init__(self):
        self.stream = MarketStreamManager()
        self.agent = QLearningAgent()
        self.last_action = None
        self.last_state = None
        self.last_reward = 0

    def get_state(self):
        """Valós idejű piaci állapot lekérése AI szempontból."""
        s = self.stream.state
        return np.array([
            s["eth_trend"],
            s["eth_vol"],
            s["btc_trend"],
            s["btc_vol"],
        ])

    def compute_reward(self, prev_price, current_price):
        if prev_price is None or current_price is None:
            return 0
        return (current_price - prev_price) / prev_price

    def step(self):
        current_state = self.get_state()
        action = self.agent.choose_action(current_state)

        # Reward szamitas
        eth_price = self.stream.state["eth_price"]
        reward = 0
        if self.last_state is not None and self.last_action is not None:
            reward = self.compute_reward(self.prev_price, eth_price)
            self.agent.learn(self.last_state, self.last_action, reward, current_state)

        self.prev_price = eth_price
        self.last_state = current_state
        self.last_action = action
        self.last_reward = reward

        return {
            "action": action,
            "reward": reward,
            "trend": self.stream.state["eth_trend"],
            "vol": self.stream.state["eth_vol"],
        }

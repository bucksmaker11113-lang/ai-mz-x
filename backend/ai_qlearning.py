# ai_qlearning.py
# MZ/X – Q-learning Agent (5-action rendszer: HOLD, Light LONG/SHORT, Strong LONG/SHORT)

import numpy as np
import random
import settings

class QLearningAgent:
    def __init__(self, state_size=4, action_size=5):
        self.state_size = state_size
        self.action_size = action_size

        # Q-tábla inicializálása
        self.q_table = np.zeros((200, action_size))  # Dinamikus discretization

        # Q-learning paraméterek
        self.alpha = 0.1      # tanulási ráta
        self.gamma = 0.95     # diszkont faktor
        self.epsilon = 0.15   # exploration ráta (élő módban alacsony)

    # ---- Állapot diszkretizálása ----
    def discretize_state(self, state):
        trend_eth = int(state[0] * 100)     # 0–100 skála
        vol_eth = int(state[1] * 100)
        trend_btc = int(state[2] * 100)
        vol_btc = int(state[3] * 100)

        # Egy dimenzióra vetítés
        idx = int((trend_eth * 0.4) + (vol_eth * 0.3) + (trend_btc * 0.2) + (vol_btc * 0.1))
        idx = max(0, min(199, idx))
        return idx

    # ---- Akció kiválasztása ----
    def choose_action(self, state):
        idx = self.discretize_state(state)

        if random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)

        return int(np.argmax(self.q_table[idx]))

    # ---- Tanulási szabály ----
    def learn(self, old_state, action, reward, new_state):
        old_idx = self.discretize_state(old_state)
        new_idx = self.discretize_state(new_state)

        q_old = self.q_table[old_idx, action]
        q_max = np.max(self.q_table[new_idx])

        # Q-learning frissítés
        self.q_table[old_idx, action] = q_old + self.alpha * (reward + self.gamma * q_max - q_old)

    # ---- Debug: Visszaadja az akció nevét ----
    def action_name(self, a):
        return [
            "HOLD",
            "LIGHT_LONG",
            "STRONG_LONG",
            "LIGHT_SHORT",
            "STRONG_SHORT",
        ][a]

// ai/qlearning.js
// MZ/X ANDROID – Natív Q-Learning AI döntésmotor
// Egyszerűsített és gyors mobil verzió (ETH / BTC kereszt trend alapján)

// Q-tábla létrehozása
// Állapot: trend szint (3 kategória) × vol szint (3 kategória)
// Akció: 0 = NOP, 1 = BUY, 2 = SELL

const STATES = 9;   // 3x3 kombináció
const ACTIONS = 3;  // NOP / BUY / SELL

// Q-mátrix inicializálás\export const Q = Array.from({ length: STATES }, () => Array(ACTIONS).fill(0));

// Hyperparaméterek
const ALPHA = 0.1;        // tanulási ráta
const GAMMA = 0.9;        // diszkontált kifizetés
const EPSILON = 0.3;      // felfedezés aránya (exploration)

// Állapot-diszkretizálás
export function getState(trend, vol) {
  let t = trend > 0.6 ? 2 : trend < 0.4 ? 0 : 1;
  let v = vol > 0.06 ? 2 : vol < 0.02 ? 0 : 1;
  return t * 3 + v; // 0–8
}

// Akció választás epsilon-greedily
export function chooseAction(state) {
  if (Math.random() < EPSILON) {
    return Math.floor(Math.random() * ACTIONS);
  }
  const row = Q[state];
  return row.indexOf(Math.max(...row));
}

// Q-value update
export function updateQ(state, action, reward, nextState) {
  const predict = Q[state][action];
  const target = reward + GAMMA * Math.max(...Q[nextState]);
  Q[state][action] = predict + ALPHA * (target - predict);
}

// Reward logika
export function getReward(lastPrice, newPrice, action) {
  if (action === 1) return newPrice - lastPrice; // BUY reward
  if (action === 2) return lastPrice - newPrice; // SELL reward
  return -0.01;                                   // NOP kis büntetés
}

// Fő döntési ciklus
export function aiDecision(lastPrice, newPrice, trend, vol) {
  const state = getState(trend, vol);
  const nextState = state;

  const action = chooseAction(state);
  const reward = getReward(lastPrice, newPrice, action);

  updateQ(state, action, reward, nextState);

  if (action === 1) return "BUY";
  if (action === 2) return "SELL";
  return "NOP";
}

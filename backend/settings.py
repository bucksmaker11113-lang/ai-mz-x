# settings.py
# MZ/X – Rendszer beállítások és konfigurációk

# === Binance WebSocket URL-ek ===
BINANCE_FUTURES_WS_ETH = "wss://fstream.binance.com/ws/ethusdc@ticker"
BINANCE_FUTURES_WS_BTC = "wss://fstream.binance.com/ws/btcusdc@ticker"

# === WebSocket reconnect beállítások ===
WS_RECONNECT_SECONDS = 3

# === Trend számítási ablak (órás adat) ===
TREND_WINDOW = 60  # 60 tick = 1 óra

# === Volatilitás szorzó vizualizációhoz ===
VOL_VISUAL_SCALE = 12

# === AI Engine konfiguráció ===
Q_LEARNING_ENABLED = True
Q_ALPHA = 0.1
Q_GAMMA = 0.95
Q_EPSILON = 0.15

# === Action Space (5-féle) ===
ACTIONS = ["HOLD", "LIGHT_LONG", "STRONG_LONG", "LIGHT_SHORT", "STRONG_SHORT"]

# === Vizuális AI CORE alapértékek ===
DEFAULT_TREND = 0.5
DEFAULT_VOL = 0.02

# === Backend frissítési intervallum ===
REALTIME_UPDATE_MS = 500

# === Debug mód ===
DEBUG = True

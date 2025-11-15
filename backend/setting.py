# settings.py
# MZ/X Trading System – Global Configuration

###############################################
# DATA SOURCES (BINANCE WEBSOCKETS)
###############################################

USE_BINANCE_FUTURES = True      # Binance Futures stream engedélyezése
USE_BINANCE_SPOT = False        # Spot stream (később opcionális)

USE_ETH = True                  # ETHUSDC futures stream használata
USE_BTC = True                  # BTCUSDC futures stream használata

###############################################
# TREND LOGIC SETTINGS (1 órás trend)
###############################################

TREND_INTERVAL_MINUTES = 60     # 1 órás adatgyűjtési ablak

# Stratégiai küszöbök (A verzió)
TREND_WEAK = 0.5                # 0.5% → gyenge trend
TREND_MEDIUM = 2.0              # 2% → közepes trend
TREND_STRONG = 5.0              # 5% → erős trend

###############################################
# AI VISUALIZATION SETTINGS (3D UI)
###############################################

VISUAL_USE_ETH_FIRST = True     # ETH vezérli a 3D AI magot
VISUAL_USE_BTC_SECONDARY = True # BTC másodlagos adatként jelenik meg

###############################################
# PERFORMANCE & SAFETY CONFIG
###############################################

AUTO_RECONNECT = True           # Automatikus reconnect engedélyezése
MAX_WS_RETRIES = 999999         # Gyakorlatilag végtelen reconnect ciklus

###############################################
# DEBUG & LOGGING
###############################################

DEBUG_WEBSOCKET = True
DEBUG_TREND = False
DEBUG_VOL = False

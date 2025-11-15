# binance_ws_btc.py
# Binance Futures BTCUSDC WebSocket stream handler

import asyncio
import json
import websockets
from collections import deque
import time
import settings

WS_URL = "wss://fstream.binance.com/ws/btcusdc@ticker"

class BTCStream:
    def __init__(self):
        self.price = None
        self.trend = 0.5
        self.volatility = 0.02

        # 1 órás árbuffer
        self.history = deque(maxlen=3600)
        self.last_update = time.time()

    async def connect(self):
        retries = 0

        while True:
            try:
                if settings.DEBUG_WEBSOCKET:
                    print("[BTC-WS] Connecting…")

                async with websockets.connect(WS_URL) as ws:
                    print("[BTC-WS] Connected to Binance Futures BTCUSDC")
                    retries = 0

                    async for msg in ws:
                        data = json.loads(msg)

                        current_price = float(data.get("c", 0))
                        price_change_percent = float(data.get("P", 0))

                        self.price = current_price

                        now = time.time()
                        if now - self.last_update >= 1:
                            self.history.append(current_price)
                            self.last_update = now

                        if len(self.history) > 10:
                            price_1h_ago = self.history[0]
                            diff = ((current_price - price_1h_ago) / price_1h_ago) * 100

                            # Trend kategorizálás stratégiai küszöbökkel
                            if abs(diff) < settings.TREND_WEAK:
                                self.trend = 0.50
                            elif abs(diff) < settings.TREND_MEDIUM:
                                self.trend = 0.60 if diff > 0 else 0.40
                            elif abs(diff) < settings.TREND_STRONG:
                                self.trend = 0.75 if diff > 0 else 0.25
                            else:
                                self.trend = 0.85 if diff > 0 else 0.15

                        # Volatilitás becslés
                        self.volatility = min(abs(price_change_percent) / 50, 0.1)

            except Exception as e:
                print(f"[BTC-WS] ERROR: {e}")
                retries += 1
                if retries > settings.MAX_WS_RETRIES:
                    print("[BTC-WS] MAX RETRIES EXCEEDED — STOPPING.")
                    return
                await asyncio.sleep(3)
                print("[BTC-WS] Reconnecting…")

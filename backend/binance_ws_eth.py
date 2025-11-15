# binance_ws_eth.py
# Binance Futures ETHUSDC WebSocket stream handler

import asyncio
import json
import websockets
from collections import deque
import time
import settings

WS_URL = "wss://fstream.binance.com/ws/ethusdc@ticker"

class ETHStream:
    def __init__(self):
        self.price = None
        self.trend = 0.5
        self.volatility = 0.02

        # Árbuffer 1 órára (60 perc = 3600 mp)
        self.history = deque(maxlen=3600)
        self.last_update = time.time()

    async def connect(self):
        retries = 0

        while True:
            try:
                if settings.DEBUG_WEBSOCKET:
                    print("[ETH-WS] Connecting…")

                async with websockets.connect(WS_URL) as ws:
                    print("[ETH-WS] Connected to Binance Futures ETHUSDC")
                    retries = 0

                    async for msg in ws:
                        data = json.loads(msg)

                        current_price = float(data.get("c", 0))
                        price_change_percent = float(data.get("P", 0))
                        vol_24h = float(data.get("Q", 0))

                        self.price = current_price

                        # Mentjük a history-t trend számításhoz
                        now = time.time()
                        if now - self.last_update >= 1:
                            self.history.append(current_price)
                            self.last_update = now

                        # Ha van elég adat 1 órára
                        if len(self.history) > 10:
                            price_1h_ago = self.history[0]
                            diff = ((current_price - price_1h_ago) / price_1h_ago) * 100

                            # Trend kalkuláció (A stratégiai küszöbök)
                            if abs(diff) < settings.TREND_WEAK:
                                self.trend = 0.50
                            elif abs(diff) < settings.TREND_MEDIUM:
                                self.trend = 0.60 if diff > 0 else 0.40
                            elif abs(diff) < settings.TREND_STRONG:
                                self.trend = 0.75 if diff > 0 else 0.25
                            else:
                                self.trend = 0.85 if diff > 0 else 0.15

                        # Vol kalkuláció (nagyon egyszerű, később pontosítható)
                        self.volatility = min(abs(price_change_percent) / 50, 0.1)

            except Exception as e:
                print(f"[ETH-WS] ERROR: {e}")
                retries += 1
                if retries > settings.MAX_WS_RETRIES:
                    print("[ETH-WS] MAX RETRIES EXCEEDED — STOPPING.")
                    return
                await asyncio.sleep(3)
                print("[ETH-WS] Reconnecting…")

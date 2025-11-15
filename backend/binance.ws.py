# binance_ws.py
import asyncio
import json
import websockets

BINANCE_WS_URL = "wss://fstream.binance.com/ws/ethusdc@ticker"

class BinanceStream:
    def __init__(self):
        self.price = None
        self.volatility = None
        self.trend = 0.5

    async def connect(self):
        while True:
            try:
                async with websockets.connect(BINANCE_WS_URL) as ws:
                    print("WS: Connected to Binance Futures")

                    async for msg in ws:
                        data = json.loads(msg)

                        price = float(data.get("c", 0))
                        vol_24h = float(data.get("P", 0))
                        volume = float(data.get("Q", 0))

                        # Trend jelzés
                        if vol_24h > 0:
                            self.trend = 0.75
                        elif vol_24h < 0:
                            self.trend = 0.25
                        else:
                            self.trend = 0.5

                        # Volatilitás
                        self.volatility = min(abs(vol_24h) / 50, 0.1)

                        self.price = price

            except Exception as e:
                print("WS ERROR:", e)
                await asyncio.sleep(3)
                print("Reconnecting WebSocket...")

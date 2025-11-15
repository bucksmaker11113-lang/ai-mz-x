# market_stream_manager.py
# MZ/X – Valós idejű Binance Futures adatmotor

import asyncio
import json
import aiohttp
from utils_logger import Log
import settings
from utils_helpers import safe_float, percent_change, avg

class MarketStreamManager:
    def __init__(self):
        self.state = {
            "eth_price": None,
            "btc_price": None,
            "eth_trend": settings.DEFAULT_TREND,
            "btc_trend": settings.DEFAULT_TREND,
            "eth_vol": settings.DEFAULT_VOL,
            "btc_vol": settings.DEFAULT_VOL,
            "visual_trend": 0.5,
            "visual_vol": 0.02,
        }

        self.eth_prices = []
        self.btc_prices = []

    async def start(self):
        Log.info("MarketStreamManager starting...")
        await asyncio.gather(
            self._stream_eth(),
            self._stream_btc(),
            self._compute_loop(),
        )

    async def _stream_eth(self):
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(settings.BINANCE_FUTURES_WS_ETH) as ws:
                        Log.ws("ETH WebSocket connected")
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                data = json.loads(msg.data)
                                price = safe_float(data.get("c"))
                                if price:
                                    self.state["eth_price"] = price
                                    self.eth_prices.append(price)
                                    if len(self.eth_prices) > settings.TREND_WINDOW:
                                        self.eth_prices.pop(0)
                            else:
                                break
            except Exception as e:
                Log.error(f"ETH stream error: {e}")
                await asyncio.sleep(settings.WS_RECONNECT_SECONDS)

    async def _stream_btc(self):
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(settings.BINANCE_FUTURES_WS_BTC) as ws:
                        Log.ws("BTC WebSocket connected")
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                data = json.loads(msg.data)
                                price = safe_float(data.get("c"))
                                if price:
                                    self.state["btc_price"] = price
                                    self.btc_prices.append(price)
                                    if len(self.btc_prices) > settings.TREND_WINDOW:
                                        self.btc_prices.pop(0)
                            else:
                                break
            except Exception as e:
                Log.error(f"BTC stream error: {e}")
                await asyncio.sleep(settings.WS_RECONNECT_SECONDS)

    async def _compute_loop(self):
        while True:
            try:
                self._compute_trends()
                self._compute_visuals()
            except Exception as e:
                Log.error(f"Compute loop error: {e}")
            await asyncio.sleep(0.5)

    def _compute_trends(self):
        if len(self.eth_prices) > 2:
            change = percent_change(self.eth_prices[0], self.eth_prices[-1])
            self.state["eth_trend"] = 0.5 + change * 10

        if len(self.btc_prices) > 2:
            change = percent_change(self.btc_prices[0], self.btc_prices[-1])
            self.state["btc_trend"] = 0.5 + change * 10

    def _compute_visuals(self):
        eth_t = self.state["eth_trend"]
        btc_t = self.state["btc_trend"]
        self.state["visual_trend"] = (eth_t * 0.7) + (btc_t * 0.3)

        if len(self.eth_prices) > 10:
            vols = [abs(self.eth_prices[i] - self.eth_prices[i-1]) for i in range(1, len(self.eth_prices))]
            vol = avg(vols)
            self.state["eth_vol"] = vol
            self.state["visual_vol"] = vol * settings.VOL_VISUAL_SCALE

// binance/realtime.js
// MZ/X ANDROID – Binance Futures USDC élő adat WebSocket (React Native / Expo)
// Mobilon futó natív websocket kliens

import { useEffect, useRef, useState } from 'react';

// Binance Futures USDC endpoint
const BINANCE_WS = "wss://fstream.binance.com/stream?streams=ethusdc@markPrice/btcusdc@markPrice";

export function useBinanceRealtime() {
  const wsRef = useRef(null);
  const [eth, setEth] = useState(null);
  const [btc, setBtc] = useState(null);
  const [trend, setTrend] = useState(0.5);
  const [vol, setVol] = useState(0.02);

  useEffect(() => {
    wsRef.current = new WebSocket(BINANCE_WS);

    wsRef.current.onopen = () => {
      console.log("Binance WS connected");
    };

    wsRef.current.onmessage = (msg) => {
      try {
        const json = JSON.parse(msg.data);
        const stream = json.stream;
        const price = parseFloat(json.data.p);

        // ETH ár frissítése
        if (stream.includes("ethusdc")) {
          if (eth !== null) {
            const diff = Math.abs(price - eth);
            setVol(Math.min(0.1, diff / 20));
            setTrend(price > eth ? 0.65 : 0.35);
          }
          setEth(price);
        }

        // BTC ár frissítése
        if (stream.includes("btcusdc")) {
          setBtc(price);
        }
      } catch (err) {
        console.log("WS parse error", err);
      }
    };

    wsRef.current.onerror = (err) => {
      console.log("Binance WS error", err);
    };

    wsRef.current.onclose = () => {
      console.log("Binance WS closed – reconnecting in 1s");
      setTimeout(() => {
        useBinanceRealtime();
      }, 1000);
    };

    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  return { eth, btc, trend, vol };
}

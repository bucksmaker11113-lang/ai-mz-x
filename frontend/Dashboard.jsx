// Dashboard.jsx
// MZ/X – 3D Neon Trading Command Center
// Mobil + Desktop reszponzív elrendezéssel

import React, { useState, useEffect } from "react";
import AICore3D from "./AICore3D";
import NeuralDataPanel from "./NeuralDataPanel";
import TradingConsole from "./TradingConsole";
import { ParticleHalo } from "./ParticleHalo";

export default function Dashboard() {
  const [trend, setTrend] = useState(0.5);
  const [vol, setVol] = useState(0.02);
  const [ethPrice, setEthPrice] = useState(null);
  const [btcPrice, setBtcPrice] = useState(null);

  // REALTIME FETCH LOOP
  useEffect(() => {
    async function loadData() {
      try {
        const res = await fetch("/realtime");
        const json = await res.json();

        if (json) {
          setTrend(json.visual_trend || 0.5);
          setVol(json.visual_vol || 0.02);
          setEthPrice(json.eth_price || null);
          setBtcPrice(json.btc_price || null);
        }
      } catch (e) {
        console.error("Realtime fetch error:", e);
      }
    }

    loadData();
    const interval = setInterval(loadData, 500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "1fr",
        gridTemplateRows: "auto auto auto",
        height: "100vh",
        overflow: "hidden",
        background: "radial-gradient(circle at center, #2b0066 0%, #120033 70%, #0a001a 100%)",
      }}
    >
      {/* === DESKTOP LAYOUT === */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "300px 1fr 300px",
          height: "100%",
          width: "100%",
          position: "relative",
        }}
        className="dashboard-desktop"
      >
        {/* Bal panel */}
        <div style={{ padding: "15px", display: "flex", flexDirection: "column", gap: "10px" }}>
          <NeuralDataPanel ethPrice={ethPrice} btcPrice={btcPrice} trend={trend} vol={vol} />
        </div>

        {/* Központi 3D UI */}
        <div style={{ position: "relative" }}>
          <div style={{ position: "absolute", inset: 0 }}>
            <AICore3D trend={trend} vol={vol} />
          </div>
          <div style={{ position: "absolute", inset: 0 }}>
            <ParticleHalo vol={vol} />
          </div>
        </div>

        {/* Jobb oldali konzol */}
        <div style={{ padding: "15px", display: "flex", flexDirection: "column", gap: "10px" }}>
          <TradingConsole ethPrice={ethPrice} btcPrice={btcPrice} />
        </div>
      </div>

      {/* === MOBIL LAYOUT === */}
      <style>
        {`
          @media (max-width: 900px) {
            .dashboard-desktop {
              grid-template-columns: 1fr;
              grid-template-rows: auto auto auto;
            }
          }
        `}
      </style>
    </div>
  );
}

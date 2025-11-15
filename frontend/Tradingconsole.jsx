// TradingConsole.jsx
// MZ/X – Jobb oldali holografikus Trading Console panel

import React from "react";

export default function TradingConsole({ ethPrice, btcPrice }) {
  return (
    <div
      style={{
        padding: "20px",
        borderRadius: "16px",
        background: "rgba(0, 120, 140, 0.35)",
        border: "1px solid rgba(0, 255, 255, 0.35)",
        backdropFilter: "blur(10px)",
        color: "#eaffff",
        boxShadow: "0 0 20px rgba(0,255,255,0.4)",
      }}
    >
      <h2 style={{ marginBottom: "10px", fontSize: "20px" }}>Kereskedési Konzol</h2>

      <div style={{ marginBottom: "10px", fontSize: "16px" }}>
        <strong>ETH ár:</strong> {ethPrice ? ethPrice.toFixed(2) + " USDC" : "betöltés..."}
      </div>

      <div style={{ marginBottom: "10px", fontSize: "16px" }}>
        <strong>BTC ár:</strong> {btcPrice ? btcPrice.toFixed(2) + " USDC" : "betöltés..."}
      </div>

      <div style={{ marginBottom: "10px", fontSize: "16px" }}>
        <strong>Pozíció:</strong> nincs megnyitva
      </div>

      <div style={{ marginBottom: "10px", fontSize: "16px" }}>
        <strong>AI döntés:</strong> (hamarosan integrálható)
      </div>

      <div style={{ fontSize: "14px", opacity: 0.8 }}>
        Élő Binance Futures adatfolyam alapján.
      </div>
    </div>
  );
}

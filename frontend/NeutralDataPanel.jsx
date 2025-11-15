// NeuralDataPanel.jsx
// MZ/X – Bal oldali holografikus AI adatpanel

import React from "react";

export default function NeuralDataPanel({ ethPrice, btcPrice, trend, vol }) {
  const trendText =
    trend > 0.55 ? "Erős emelkedés" : trend < 0.45 ? "Csökkenő trend" : "Oldalazás";

  return (
    <div
      style={{
        padding: "20px",
        borderRadius: "16px",
        background: "rgba(80, 0, 120, 0.35)",
        border: "1px solid rgba(255, 0, 255, 0.3)",
        backdropFilter: "blur(10px)",
        color: "#fff",
        boxShadow: "0 0 20px rgba(200,0,255,0.4)",
      }}
    >
      <h2 style={{ marginBottom: "10px", fontSize: "20px" }}>Neurális PIACI ADATOK</h2>

      <div style={{ marginBottom: "8px", fontSize: "16px" }}>
        <strong>ETH ár:</strong> {ethPrice ? ethPrice.toFixed(2) + " USDC" : "betöltés..."}
      </div>

      <div style={{ marginBottom: "8px", fontSize: "16px" }}>
        <strong>BTC ár:</strong> {btcPrice ? btcPrice.toFixed(2) + " USDC" : "betöltés..."}
      </div>

      <div style={{ marginBottom: "8px", fontSize: "16px" }}>
        <strong>Trend:</strong> {trendText}
      </div>

      <div style={{ marginBottom: "8px", fontSize: "16px" }}>
        <strong>Volatilitás:</strong> {(vol * 100).toFixed(2)}%
      </div>
    </div>
  );
}

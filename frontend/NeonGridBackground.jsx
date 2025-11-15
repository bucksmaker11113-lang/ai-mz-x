// NeonGridBackground.jsx
// MZ/X – Futurisztikus neon grid háttér animáció

import React from "react";

export default function NeonGridBackground() {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 0,
        background:
          "linear-gradient(90deg, rgba(0,255,255,0.15) 1px, transparent 1px), linear-gradient(0deg, rgba(0,255,255,0.15) 1px, transparent 1px)",
        backgroundSize: "40px 40px",
        animation: "gridMove 12s linear infinite",
      }}
    >
      <style>
        {`
        @keyframes gridMove {
          0% { background-position: 0 0, 0 0; }
          100% { background-position: 80px 80px, 80px 80px; }
        }
      `}
      </style>
    </div>
  );
}

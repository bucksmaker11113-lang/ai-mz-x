// HoloOverlay.jsx
// MZ/X – Holografikus overlay réteg (finom animált zaj és fényglitch)

import React from "react";

export default function HoloOverlay() {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        pointerEvents: "none",
        zIndex: 2,
        background:
          "linear-gradient( to bottom, rgba(255,0,255,0.08), rgba(0,200,255,0.05) )",
        mixBlendMode: "screen",
        animation: "holoFlicker 4s infinite ease-in-out",
      }}
    >
      <style>
        {`
        @keyframes holoFlicker {
          0% { opacity: 0.25; }
          30% { opacity: 0.35; }
          50% { opacity: 0.28; }
          70% { opacity: 0.38; }
          100% { opacity: 0.25; }
        }
        
        @keyframes scanline {
          0% { transform: translateY(-100%); }
          100% { transform: translateY(100%); }
        }
        `}
      </style>

      {/* Futó scanline effektek */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          background:
            "repeating-linear-gradient(to bottom, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 1px, transparent 2px, transparent 4px)",
          animation: "scanline 6s linear infinite",
          opacity: 0.7,
        }}
      />
    </div>
  );
}

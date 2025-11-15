// App.jsx
// MZ/X Frontend Root – 3D Neon Trading Command Center

import React from "react";
import Dashboard from "./Dashboard";
import NeonGridBackground from "./NeonGridBackground";
import HoloOverlay from "./HoloOverlay";

export default function App() {
  return (
    <div style={{ width: "100vw", height: "100vh", overflow: "hidden" }}>
      <NeonGridBackground />
      <HoloOverlay />
      <Dashboard />
    </div>
  );
}

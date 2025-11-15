import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// MZ/X – Vite konfiguráció (frontend build + deploy kompatibilitás)

export default defineConfig({
  plugins: [react()],

  server: {
    port: 5173,
    open: true,
  },

  // Railway / Render kompatibilis build
  build: {
    outDir: "dist",
  },

  // Backend proxy fejlesztői módban
  proxy: {
    "/realtime": "http://localhost:8000",
    "/chat": "http://localhost:8000",
  },
});
// main.jsx
// MZ/X – Frontend belépési pont (React + Vite)

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);


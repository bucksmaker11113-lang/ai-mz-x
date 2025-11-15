# main.py
# MZ/X – FastAPI backend + Binance Futures stream manager + Q-learning AI

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers_chat_routes import router as chat_router
from market_stream_manager import MarketStreamManager
from utils_logger import Log
import uvicorn

app = FastAPI(title="MZ/X Trading AI Backend")

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ROUTERS =====
app.include_router(chat_router)

# ===== GLOBAL STREAM MANAGER INSTANCE =====
manager = MarketStreamManager()

# ===== REALTIME ENDPOINT =====
@app.get("/realtime")
def realtime_data():
    return manager.state

# ===== BACKGROUND TASK =====
@app.on_event("startup")
def startup_event():
    Log.info("MZ/X Backend indul...")
    loop = asyncio.get_event_loop()
    loop.create_task(manager.start())

# ===== MAIN ENTRY POINT =====
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

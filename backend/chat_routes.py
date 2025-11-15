# chat_routes.py
# MZ/X – Kétirányú AI kommunikációs modul (FastAPI Router)

from fastapi import APIRouter
from pydantic import BaseModel
from market_stream_manager import MarketStreamManager
import settings

router = APIRouter()

# ====== Adatmodell a bejövő üzenetekhez ======
class UserMessage(BaseModel):
    message: str

# ====== Egyszerű AI válasz logika (később cserélhető) ======
def generate_ai_reply(user_text: str, state):
    trend = state.get("eth_trend", 0.5)
    vol = state.get("eth_vol", 0.02)
    price = state.get("eth_price", None)

    # Egyszerű intelligens válasz logika
    if price:
        if trend > 0.6:
            return f"Jelenleg emelkedő irány dominál az ETH piacon. Ár: {price:.2f} USDC. Volatilitás: {vol:.3f}."
        elif trend < 0.4:
            return f"Csökkenő trend figyelhető meg az ETH piacon. Ár: {price:.2f} USDC. Volatilitás: {vol:.3f}."
        else:
            return f"Oldalazás látható. ETH ár: {price:.2f} USDC. Vol: {vol:.3f}. Mit szeretnél elemezni?"

    return "Az AI jelenleg tölti a valós idejű adatokat. Kérlek próbáld meg pár másodperc múlva."

# ====== CHAT ENDPOINT ======
@router.post("/chat")
def chat_with_ai(msg: UserMessage):
    """
    Kétirányú beszélgetés MZ/X AI-val.
    Kimenet: AI válasza + valós idejű ETH/BTC állapot.
    """
    manager = MarketStreamManager()  # Singleton lenne ideális, de egyszerűsített

    ai_reply = generate_ai_reply(msg.message, manager.state)

    return {
        "user": msg.message,
        "ai_reply": ai_reply,
        "state": manager.state,
    }


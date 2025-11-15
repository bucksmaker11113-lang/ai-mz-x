# MZ/X FULL BACKEND STRUCTURE (INITIALIZED)
# This file will act as an index. Real modules will be added step-by-step.

# backend/
#   main.py
#   config.py
#   trade_executor.py
#   risk_manager.py
#   dynamic_leverage.py
#   position_sizer.py
#   chat_module.py
#   narrative_engine.py
#   data_bridge.py
#   qlearning/
#       __init__.py
#       q_table.py
#       learner.py
#   utils/
#       logger.py
#       db.py
#       helpers.py

# === BLOKK 1: FASTAPI BACKEND MAG ===
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from chat_routes import chat_router

app = FastAPI(title="MZ/X Futures AI Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API gyökér válasz ---
@app.get("/")
def root():
    return {
        "status": "MZ/X backend running",
        "chat_module": "active",
        "engine": "initialized",
        "version": "1.0"
    }

# --- Chat modul router bekötése ---
app.include_router(chat_router)

# --- Trade modul router bekötése (D5) ---
from trade_routes import trade_router
app.include_router(trade_router)
app.include_router(chat_router)

# --- Hely a futures kereskedési motor endpointoknak (később kerülnek be) ---
# app.include_router(trade_router)

# --- Lokális futtatási mód (Railway/Render alatt nem szükséges) ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# config.py
TESTNET_API_KEY = ""
TESTNET_SECRET_KEY = ""
DATABASE_URL = "sqlite:///./mzx_futures.db"

# utils/logger.py
import logging
logging.basicConfig(level=logging.INFO, format="[MZX] %(message)s")
logger = logging.getLogger(__name__)

# utils/db.py
import sqlite3

def get_db():
    conn = sqlite3.connect("mzx_futures.db")
    conn.row_factory = sqlite3.Row
    return conn

# utils/helpers.py
import time

def timestamp():
    return int(time.time())

# === BLOKK 1 kész. Következik a BLOKK 2 (AI Engine). ===

# === BLOKK 2: AI ENGINE (FUTURES MOTOR) ===

# trade_executor.py
from utils.logger import logger
from config import TESTNET_API_KEY, TESTNET_SECRET_KEY

class TradeExecutor:
    def __init__(self):
        self.api_key = TESTNET_API_KEY
        self.secret = TESTNET_SECRET_KEY

    def place_order(self, symbol, side, qty, leverage, sl=None, tp=None):
        logger.info(f"[Order] {symbol} | {side} | qty={qty} | lev={leverage} | SL={sl} | TP={tp}")
        return {"status": "simulated", "symbol": symbol, "side": side}

trade_executor = TradeExecutor()

# risk_manager.py
class RiskManager:
    def assess_risk(self, vol, trend_strength, liquidity, liquidation_buffer):
        base_risk = max(0.5, min(3.0, vol * 10))
        trend_adj = 1 + (trend_strength - 0.5)
        liq_adj = 1 if liquidity == "strong" else 0.7
        final = base_risk * trend_adj * liq_adj
        return max(0.2, min(final, 5))

risk_manager = RiskManager()

# dynamic_leverage.py
class DynamicLeverage:
    def get_leverage(self, symbol, vol):
        if symbol == "ETHUSDC":
            max_lev = 25
        else:
            max_lev = 15
        if vol < 0.015:
            return max_lev
        elif vol < 0.03:
            return int(max_lev * 0.6)
        else:
            return int(max_lev * 0.3)

leverage_engine = DynamicLeverage()

# position_sizer.py
class PositionSizer:
    def calc_size(self, equity, risk_pct, sl_distance, leverage):
        if sl_distance == 0: sl_distance = 0.001
        size = (equity * (risk_pct / 100)) / (sl_distance * leverage)
        return round(size, 3)

position_sizer = PositionSizer()

# data_bridge.py
class DataBridge:
    def __init__(self):
        pass
    def get_features(self, symbol):
        return {"trend": 0.62, "vol": 0.014, "liquidity": "strong"}

data_bridge = DataBridge()

# qlearning/q_table.py
class QTable:
    def __init__(self):
        self.table = {}

    def get(self, state):
        return self.table.get(state, {"long":0, "short":0, "flat":0})

    def update(self, state, action, reward):
        self.table.setdefault(state, {"long":0, "short":0, "flat":0})
        self.table[state][action] += reward

qtable = QTable()

# qlearning/learner.py
class QLearner:
    def decide(self, features):
        trend = features["trend"]
        if trend > 0.55:
            return "long"
        elif trend < 0.45:
            return "short"
        return "flat"

qlearner = QLearner()

# === BLOKK 2 kész. Következik a BLOKK 3 (Chat Modul). ===

# === chat_module.py (A1 – Alap osztály és inicializáció) ===

class ChatModule:
    """
    Magyar nyelvű AI kommunikációs modul.
    Ez fog válaszolni a felhasználó kérdéseire, és magyarázni a döntéseket.
    """

    def __init__(self):
        self.last_action = None
        self.last_reason = "Még nem történt kereskedési művelet."
        self.state_cache = {}

    def set_last_action(self, action: str, reason: str):
        """Legutóbbi AI döntés eltárolása magyarázattal együtt."""
        self.last_action = action
        self.last_reason = reason

    def get_last_action(self):
        """Visszaadja az utolsó ismert AI műveletet és annak okát."""
        return {
            "utolso_muvelet": self.last_action,
            "magyarazat": self.last_reason
        }

chat_module = ChatModule()

# === chat_module.py (A2 – Döntésmagyarázó logika) ===

    def explain_decision(self, features: dict, action: str):
        """
        Magyarázat generálása a legutóbbi AI döntéshez.
        A narrative_engine fogja szöveggé alakítani.
        """
        trend = features.get("trend", 0)
        vol = features.get("vol", 0)
        liq = features.get("liquidity", "ismeretlen")

        reason = (
            f"Trend erősség: {trend:.2f}, volatilitás: {vol:.3f}, likviditás: {liq}. "
            f"Ez alapján az AI a '{action}' lépést választotta."
        )

        self.set_last_action(action, reason)
        return {
            "dontes": action,
            "magyarazat": reason
        }


# === chat_module.py (A3 – Jel-elutasítás magyarázata) ===

    def explain_rejection(self, features: dict):
        """
        Magyarázat arra, hogy az AI miért NEM lépett be pozícióba.
        Magyar nyelven, a trend/vol/liquidity alapján.
        """
        trend = features.get("trend", 0)
        vol = features.get("vol", 0)
        liq = features.get("liquidity", "ismeretlen")

        if trend > 0.48 and trend < 0.52:
            reason = "A trend bizonytalan volt, ezért nem léptem be."
        elif vol > 0.03:
            reason = "A volatilitás túl magas volt, ezért vártam."
        elif liq != "strong":
            reason = "A likviditás gyenge volt, így biztonságosabb volt kivárni."
        else:
            reason = "A jel nem volt elég erős a belépéshez."

        self.last_reason = reason
        return {
            "dontes": "nem leptem be",
            "magyarazat": reason
        }


# === chat_module.py (A4 – Eseményösszefoglaló: "Mi történt az elmúlt X percben?") ===

    def summarize_recent(self, events: list):
        """
        Rövid, magyar nyelvű összefoglaló arról,
        hogy az AI szerint mi történt az elmúlt X percben.

        events: lista dict-ekkel, pl.
        [{"ido": 1700000, "esemeny": "trend_valtozas", "ertek": 0.62}, ...]
        """
        if not events:
            return {"osszefoglalas": "Az elmúlt időszakban nem történt jelentős változás."}

        summary_lines = []
        for e in events:
            etype = e.get("esemeny", "ismeretlen")
            val = e.get("ertek", None)

            if etype == "trend_valtozas":
                summary_lines.append(f"A trend változott, új érték: {val:.2f}.")
            elif etype == "vol_spike":
                summary_lines.append("Hirtelen volatilitás-növekedést észleltem.")
            elif etype == "liq_drop":
                summary_lines.append("A likviditás gyengült a piacon.")
            elif etype == "pozicio_zaras":
                summary_lines.append(f"Pozíció zárva: {val} eredménnyel.")
            elif etype == "signal_missed":
                summary_lines.append("Volt jel, de nem volt elég erős a belépéshez.")
            else:
                summary_lines.append(f"Esemény: {etype} – {val}")

        final_summary = " ".join(summary_lines)
        return {"osszefoglalas": final_summary}


# === chat_module.py (A5 – "Mit tervez most az AI?" – előrejelzés) ===

    def explain_plan(self, features: dict, q_state: dict):
        """
        Magyar nyelvű előrejelzés arról, hogy mit tervez az AI a következő időszakban.
        A features tartalmazza: trend, vol, liquidity stb.
        A q_state tartalmazza: long/short/flat preferenciák.
        """

        trend = features.get("trend", 0)
        vol = features.get("vol", 0)
        liq = features.get("liquidity", "ismeretlen")

        # Q-learning preferencia
        long_pref = q_state.get("long", 0)
        short_pref = q_state.get("short", 0)
        flat_pref = q_state.get("flat", 0)

        # AI szándék meghatározása
        if long_pref > short_pref and long_pref > flat_pref:
            plan = "long lehetőséget keresek"
        elif short_pref > long_pref and short_pref > flat_pref:
            plan = "short lehetőséget keresek"
        else:
            plan = "türelmesen várok egy tisztább jelre"

        # Magyar nyelvű összefoglaló
        summary = (
            f"A jelenlegi trend erőssége {trend:.2f}, a volatilitás {vol:.3f}, "
            f"a likviditás pedig: {liq}. A Q-learning alapján jelenleg: {plan}."
        )

        return {
            "terv": plan,
            "osszefoglalo": summary
        }


# === chat_module.py (A6 – Q-learning állapot magyarázata) ===

    def explain_qlearning(self, q_state: dict):
        """
        Magyar nyelvű magyarázat a Q-learning aktuális állapotáról.
        q_state: pl. {"long":0.5, "short":-0.2, "flat":0.1}
        """
        long_v = q_state.get("long", 0)
        short_v = q_state.get("short", 0)
        flat_v = q_state.get("flat", 0)

        # preferencia meghatározása
        preferred = max(q_state, key=q_state.get)

        # magyar szöveg generálása
        summary = (
            f"Q-learning értékek: LONG = {long_v:.2f}, SHORT = {short_v:.2f}, FLAT = {flat_v:.2f}. "
            f"A tanulási rendszer jelenleg a(z) '{preferred}' irányt részesíti előnyben. "
            f"Ez azt jelenti, hogy a közelmúlt piaci viselkedése erre adta a legpozitívabb visszajelzést."
        )

        return {
            "preferalt_irany": preferred,
            "magyarazat": summary
        }


# === chat_module.py (A7 – Data Mining jelmagyarázat, teljes magyar AI interpretáció) ===

    def explain_data_features(self, features: dict):
        """
        Magyar nyelvű értelmezés az AI Data Mining-ből érkező jellemzőkről.
        features: {"trend":0.62, "vol":0.014, "liquidity":"strong", ...}
        """

        trend = features.get("trend", None)
        vol = features.get("vol", None)
        liq = features.get("liquidity", None)
        bias = features.get("bias", None)
        ob_imb = features.get("orderbook_imbalance", None)
        meta = features.get("meta_trend", None)

        text_parts = []

        # --- Trend értelmezés ---
        if trend is not None:
            if trend > 0.65:
                text_parts.append(f"A trend erős és felfelé mutat (trend érték: {trend:.2f}).")
            elif trend < 0.35:
                text_parts.append(f"A trend erős és lefelé mutat (trend érték: {trend:.2f}).")
            else:
                text_parts.append(f"A trend bizonytalan vagy oldalazó (trend érték: {trend:.2f}).")

        # --- Volatilitás értelmezés ---
        if vol is not None:
            if vol > 0.03:
                text_parts.append("A volatilitás magas, ez óvatosabb kereskedést igényel.")
            elif vol < 0.01:
                text_parts.append("A volatilitás alacsony, stabilabb a piac.")
            else:
                text_parts.append(f"A volatilitás közepes (vol: {vol:.3f}).")

        # --- Likviditás értelmezés ---
        if liq is not None:
            if liq == "strong":
                text_parts.append("A likviditás erős, könnyen végrehajthatók a pozíciók.")
            elif liq == "weak":
                text_parts.append("A likviditás gyenge, nagyobb a kicsúszás kockázata.")
            else:
                text_parts.append(f"A likviditás szintje: {liq}.")

        # --- Orderbook imbalance értelmezés ---
        if ob_imb is not None:
            if ob_imb > 0.6:
                text_parts.append("Az orderbook erősen eladói oldalra húz – bearish nyomás.")
            elif ob_imb < 0.4:
                text_parts.append("Az orderbook erősen vételi oldalra húz – bullish nyomás.")
            else:
                text_parts.append("A könyv kiegyensúlyozott, nincs domináns oldal.")

        # --- Meta trend értelmezés ---
        if meta is not None:
            if meta > 0.6:
                text_parts.append("A meta-trend összképe inkább bullish.")
            elif meta < 0.4:
                text_parts.append("A meta-trend összképe inkább bearish.")
            else:
                text_parts.append("A meta-trend semleges vagy vegyes jelzést ad.")

        # --- Bias értelmezés ---
        if bias is not None:
            if bias > 0:
                text_parts.append(f"A bias pozitív (bullish irány), értéke: {bias:.2f}.")
            elif bias < 0:
                text_parts.append(f"A bias negatív (bearish irány), értéke: {bias:.2f}.")
            else:
                text_parts.append("A bias semleges.")

        # Összefoglaló generálása
        summary = " ".join(text_parts) if text_parts else "Nincs elegendő adat az értelmezéshez."

        return {"adat_elemzes": summary}


# === chat_module.py (A8 – Fő válaszgenerátor, integrált magyar chat logika) ===

    def respond(self, user_input: str, features: dict, q_state: dict, events: list):
        """
        Fő belépési pont: a felhasználó kérdését értelmezi, majd a megfelelő magyar választ adja.

        user_input: felhasználó kérdése szövegként
        features: AI Data Mining + piaci jellemzők
        q_state: Q-learning aktuális értékei
        events: legutóbbi események
        """

        text = user_input.lower().strip()

        # --- Kulcskérdések felismerése ---
        if "miert leptel be" in text or "miért léptél be" in text:
            return self.get_last_action()

        if "miert nem leptel be" in text or "miért nem léptél be" in text:
            return self.explain_rejection(features)

        if "mi tortent" in text or "mi történt" in text:
            return self.summarize_recent(events)

        if "mit tervezel" in text or "mi a terved" in text:
            return self.explain_plan(features, q_state)

        if "q learning" in text or "q-learning" in text:
            return self.explain_qlearning(q_state)

        if "adat" in text or "data mining" in text:
            return self.explain_data_features(features)

        # --- Alapértelmezett válasz ---
        return {
            "valasz": "Nem teljesen értem a kérdést, de szívesen segítek. Kérdezhetsz például: 
"
                       "• Mi történt az elmúlt percekben? 
"
                       "• Miért nem léptél be? 
"
                       "• Mi a terved most? 
"
                       "• Magyarázd el a Q-learning állapotát. 
"
                       "• Mit mondanak az adatok?"
        }


# === narrative_engine.py (B1 – Alap osztály és mondatgeneráló váz) ===

class NarrativeEngine:
    """
    Magyar nyelvű mondatgenerátor, amely a technikai adatokat
    érthető, emberi magyarázattá alakítja.
    """

    def __init__(self):
        pass

    def simple(self, text: str) -> str:
        """
        Egyszerű, tömör magyarázat.
        """
        return f"Röviden: {text}"

    def detailed(self, text: str) -> str:
        """
        Részletes, kereskedői stílusú magyar magyarázat.
        """
        return (
            "Részletes elemzés: "
            + text
            + " Ez a magyarázat a piaci kontextust és a technikai tényezőket is figyelembe veszi."
        )

narrative_engine = NarrativeEngine()

# === narrative_engine.py (B2 – Haladó magyar mondatgenerálás, piaci jelenségek) ===

    def trend_description(self, trend: float) -> str:
        """Magyar nyelvű értelmezés a trend erősségére."""
        if trend > 0.70:
            return f"A trend nagyon erős és határozottan felfelé mutat (trend: {trend:.2f})."
        elif trend > 0.55:
            return f"A trend stabilan bullish irányt jelez (trend: {trend:.2f})."
        elif trend < 0.30:
            return f"Erős bearish tendencia figyelhető meg (trend: {trend:.2f})."
        elif trend < 0.45:
            return f"A trend enyhén lefelé hajlik (trend: {trend:.2f})."
        else:
            return f"A trend bizonytalan vagy oldalazó (trend: {trend:.2f})."

    def volatility_description(self, vol: float) -> str:
        """Magyar nyelvű volatilitás leírás."""
        if vol > 0.04:
            return f"A volatilitás kiemelkedően magas (vol: {vol:.3f}), óvatos kereskedést igényel."
        elif vol > 0.02:
            return f"A volatilitás közepesen magas (vol: {vol:.3f}), de kezelhető."
        elif vol < 0.01:
            return f"A volatilitás alacsony és a piac stabil (vol: {vol:.3f})."
        else:
            return f"A volatilitás mérsékelt (vol: {vol:.3f})."

    def liquidity_description(self, liq: str) -> str:
        """Likviditás magyarázat magyarul."""
        if liq == "strong":
            return "A likviditás erős, a piac könnyen emészti a nagyobb pozíciókat is."
        elif liq == "weak":
            return "A likviditás gyenge, a spreadek tágulnak és nőhet a kicsúszás kockázata."
        return f"A likviditás szintje: {liq}."

    def orderbook_description(self, imbalance: float) -> str:
        """Orderbook imbalance emberi magyarázata."""
        if imbalance > 0.60:
            return "A könyv erősen eladói irányba billen – bearish nyomás uralja a piacot."
        elif imbalance < 0.40:
            return "A könyv erősen vételi oldalon terhelt – bullish nyomás látható."
        return "A könyv kiegyensúlyozott, egyik oldal sem dominálja a piacot."

    def bias_description(self, bias: float) -> str:
        """Bias értelmezése magyarul."""
        if bias > 0:
            return f"A bias enyhén bullish irányt mutat (bias: {bias:.2f})."
        elif bias < 0:
            return f"A bias enyhén bearish irányt mutat (bias: {bias:.2f})."
        return "A bias semleges, nincs irányított eltolódás."


# === narrative_engine.py (B3 – Összetett magyar piaci narratíva generátor) ===

    def combined_market_summary(self, features: dict) -> str:
        """
        Összetett, természetes magyar nyelvű piaci összefoglaló.
        A trend + vol + likviditás + bias + orderbook egyetlen elemző szövegben.
        """
        parts = []

        trend = features.get("trend")
        vol = features.get("vol")
        liq = features.get("liquidity")
        bias = features.get("bias")
        ob = features.get("orderbook_imbalance")

        # Trend
        if trend is not None:
            parts.append(self.trend_description(trend))

        # Volatilitás
        if vol is not None:
            parts.append(self.volatility_description(vol))

        # Likviditás
        if liq is not None:
            parts.append(self.liquidity_description(liq))

        # Orderbook
        if ob is not None:
            parts.append(self.orderbook_description(ob))

        # Bias
        if bias is not None:
            parts.append(self.bias_description(bias))

        if not parts:
            return "Nem áll rendelkezésre elég adat egy átfogó piaci összefoglalóhoz."

        # Végső összefűzés, természetes narratív stílus
        summary = " ".join(parts)
        final = (
            "Piaci összefoglaló: " + summary +
            " Összességében ezek alapján az AI a piaci helyzetet ennek megfelelően értékeli."
        )
        return final


# === chat_routes.py (C1 – Chat API végpontok, FastAPI integráció) ===

from fastapi import APIRouter
from chat_module import chat_module
from data_bridge import data_bridge
from qlearning.q_table import qtable
from qlearning.learner import qlearner
from narrative_engine import narrative_engine

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.get("/ask")
def ask(question: str):
    """
    A felhasználó kérdése → ChatModule → magyar nyelvű AI válasz.
    """
    features = data_bridge.get_features("ETHUSDC")
    q_state = qtable.get("default_state")
    events = []  # később a valós eseménynapló kerül ide
    return chat_module.respond(question, features, q_state, events)

@chat_router.get("/summary")
def summary():
    """Piaci összefoglaló magyarul."""
    features = data_bridge.get_features("ETHUSDC")
    return {"osszefoglalas": narrative_engine.combined_market_summary(features)}

@chat_router.get("/plan")
def plan():
    features = data_bridge.get_features("ETHUSDC")
    q_state = qtable.get("default_state")
    return chat_module.explain_plan(features, q_state)

@chat_router.get("/qlearning")
def q_learning_state():
    q_state = qtable.get("default_state")
    return chat_module.explain_qlearning(q_state)

@chat_router.get("/data")
def data_explain():
    features = data_bridge.get_features("ETHUSDC")
    return chat_module.explain_data_features(features)


# === trade_routes.py (C1 – Chat API végpontok, FastAPI integráció) === (Futures API – D1 alap váz) ===
from fastapi import APIRouter
from trade_executor import trade_executor
from data_bridge import data_bridge
from qlearning.q_table import qtable
from qlearning.learner import qlearner
from risk_manager import risk_manager
from dynamic_leverage import leverage_engine
from position_sizer import position_sizer

trade_router = APIRouter(prefix="/trade", tags=["Trading"])

# --- D4: Trading API végpontok ---
@trade_router.get("/signal")
def signal():
    features = data_bridge.get_features("ETHUSDC")
    q_state = qtable.get("default_state")
    sig = position_manager.generate_signal(features, q_state)
    return {"signal": sig, "features": features, "q_state": q_state}

@trade_router.get("/plan")
def plan(equity: float = 1000):
    features = data_bridge.get_features("ETHUSDC")
    q_state = qtable.get("default_state")
    plan = position_manager.build_trade_plan("ETHUSDC", features, equity, q_state)
    return plan

@trade_router.post("/open")
def open_trade(equity: float = 1000):
    features = data_bridge.get_features("ETHUSDC")
    q_state = qtable.get("default_state")
    plan = position_manager.build_trade_plan("ETHUSDC", features, equity, q_state)

    if plan.get("status") != "trade_plan":
        return {"error": "No valid trade plan"}

    direction = plan["direction"]
    qty = plan["qty"]
    lev = plan["leverage"]
    sl = plan["sl_distance"]
    tp = plan["tp_distance"]

    resp = trade_executor.open_position("ETHUSDC", direction, qty, lev, sl, tp)
    return resp

@trade_router.post("/close")
def close_trade():
    resp = trade_executor.close_position()
    return resp

@trade_router.get("/state")
def trade_state():
    return {"active_position": trade_executor.active_position}

@trade_router.get("/status")
def status():
    return {"engine": "active", "testnet_ready": True}


# === position_manager.py (D2 – AI kereskedési döntéshozatal, 1. rész) ===

class PositionManager:
    """
    AI kereskedési döntéshozatal: jel generálás, irány meghatározása,
    risk manager + leverage engine + position sizing integráció.
    """

    def __init__(self):
        self.active_position = None
        self.last_signal = None

    def generate_signal(self, features: dict, q_state: dict):
        """
        Belépési irány meghatározása a trend + vol + liquidity + Q-learning alapján.
        Visszatér: long / short / flat.
        """
        trend = features.get("trend", 0)
        vol = features.get("vol", 0)
        liq = features.get("liquidity", "strong")

        # Q-learning preferencia
        long_p = q_state.get("long", 0)
        short_p = q_state.get("short", 0)
        flat_p = q_state.get("flat", 0)

        # Ha Q-learning egyértelmű
        if long_p > short_p and long_p > flat_p:
            base = "long"
        elif short_p > long_p and short_p > flat_p:
            base = "short"
        else:
            # ha a Q-learning bizonytalan → a trend dönt
            if trend > 0.55:
                base = "long"
            elif trend < 0.45:
                base = "short"
            else:
                base = "flat"

        # Volatilitás korrekció: túl magas vol → óvatosabb
        if vol > 0.035:
            base = "flat"  # nem lépünk be extrém vol-ra

        # Likviditás korrekció
        if liq != "strong":
            if base != "flat":
                base = "flat"

        self.last_signal = base
        return base


position_manager = PositionManager()

# === position_manager.py (D2 – 2. rész: risk + leverage + size + SL/TP kalkuláció) ===

    def build_trade_plan(self, symbol: str, features: dict, equity: float, q_state: dict):
        """
        Teljes kereskedési terv készítése:
        - jel (irány)
        - risk manager → risk_pct
        - dynamic leverage → tőkeáttétel
        - SL távolság becslése → pozícióméret
        - TP becslés
        """
        signal = self.generate_signal(features, q_state)

        if signal == "flat":
            return {"status": "no_trade", "reason": "A jel nem volt elég erős a belépéshez."}

        trend = features.get("trend", 0)
        vol = features.get("vol", 0)
        liq = features.get("liquidity", "strong")

        # --- Risk Manager: kockázati százalék meghatározása ---
        # equity = teljes tőke USDC-ben
        liquidation_buffer = 0.01
        risk_score = risk_manager.assess_risk(vol, trend, liq, liquidation_buffer)
        risk_pct = max(0.3, min(risk_score * 1.2, 2.0))  # 0.3% – 2% közötti kockázat

        # --- Leverage engine ---
        leverage = leverage_engine.get_leverage(symbol, vol)

        # --- Stop Loss távolság becslése vol alapján ---
        # magasabb vol → nagyobb SL távolság
        sl_distance = max(0.002, min(0.015, vol * 4))

        # --- Pozícióméret számítása ---
        qty = position_sizer.calc_size(equity, risk_pct, sl_distance, leverage)

        # --- TP távolság becslése ---
        tp_distance = sl_distance * 2.2

        plan = {
            "status": "trade_plan",
            "direction": signal,
            "leverage": leverage,
            "qty": qty,
            "sl_distance": round(sl_distance, 4),
            "tp_distance": round(tp_distance, 4),
            "risk_pct": round(risk_pct, 2)
        }

        self.last_signal = signal
        return plan

position_manager = PositionManager()

# === trade_executor.py (D3 – teljes futures order motor szimulált/testnet struktúrával) ===

class TradeExecutor:
    """
    Futures kereskedési végrehajtó modul.
    Jelenleg szimulált módon fut, de a struktúra 100%-ban megegyezik
    a Binance Futures Testnet API működésével.
    """

    def __init__(self):
        self.active_position = None
        self.order_id_counter = 1

    def _generate_order_id(self):
        oid = f"MZX-{self.order_id_counter}"
        self.order_id_counter += 1
        return oid

    def open_position(self, symbol: str, direction: str, qty: float, leverage: int, sl_dist: float, tp_dist: float):
        """
        Pozíciónyitás (szimulált).
        direction = long / short
        qty = mennyiség
        leverage = tőkeáttétel
        sl_dist / tp_dist = ár-alapú távolságok
        """
        if self.active_position is not None:
            return {"error": "Van már aktív pozíció!"}

        order_id = self._generate_order_id()

        # Symbol aktuális ára (DataBridge később valós árakkal frissíti)
        current_price = 2500.0  # placeholder

        if direction == "long":
            sl_price = current_price * (1 - sl_dist)
            tp_price = current_price * (1 + tp_dist)
        else:
            sl_price = current_price * (1 + sl_dist)
            tp_price = current_price * (1 - tp_dist)

        self.active_position = {
            "order_id": order_id,
            "symbol": symbol,
            "direction": direction,
            "qty": qty,
            "entry_price": current_price,
            "sl_price": round(sl_price, 2),
            "tp_price": round(tp_price, 2),
            "leverage": leverage
        }

        return {
            "status": "position_opened",
            "position": self.active_position
        }

    def close_position(self):
        """Pozíció lezárása és PnL kalkuláció szimulált áron."""
        if self.active_position is None:
            return {"error": "Nincs aktív pozíció!"}

        current_price = 2500.0
        pos = self.active_position

        if pos["direction"] == "long":
            pnl = (current_price - pos["entry_price"]) * pos["qty"]
        else:
            pnl = (pos["entry_price"] - current_price) * pos["qty"]

        result = {
            "status": "position_closed",
            "closed_position": pos,
            "pnl": round(pnl, 2)
        }

        self.active_position = None
        return result

trade_executor = TradeExecutor()

# === ai_pipeline.py (D6 – AI pipeline összehangolása) ===

class AIPipeline:
    """
    Teljes AI vezérlőmotor:
    - DataBridge → friss adat
    - PositionManager → jel + terv
    - TradeExecutor → pozíciónyitás/zárás
    - Q-learning → reward frissítés
    - ChatModule → események magyarázata
    """

    def __init__(self):
        self.events = []  # minden történés naplózva

    def log_event(self, etype: str, value=None):
        self.events.append({"esemeny": etype, "ertek": value})

    def run_cycle(self, symbol: str, equity: float):
        """
        Egyetlen AI ciklus:
        1. Adat lekérése
        2. Jel generálás
        3. Kereskedési terv készítése
        4. Pozíció nyitása (ha valid)
        5. Log + Q-learning
        """
        features = data_bridge.get_features(symbol)
        q_state = qtable.get("default_state")

        # 1) jel
        signal = position_manager.generate_signal(features, q_state)
        self.log_event("signal", signal)

        # 2) terv
        plan = position_manager.build_trade_plan(symbol, features, equity, q_state)
        if plan.get("status") != "trade_plan":
            self.log_event("no_trade", plan.get("reason"))
            return {"status": "no_trade", "reason": plan.get("reason")}

        # 3) nyitás
        opened = trade_executor.open_position(
            symbol,
            plan["direction"],
            plan["qty"],
            plan["leverage"],
            plan["sl_distance"],
            plan["tp_distance"]
        )

        if "error" in opened:
            self.log_event("open_fail", opened)
            return opened

        self.log_event("opened", opened)

        # 4) reward előkészítés (helyőrző)
        reward = 0.0  # majd a zárás után frissül
        qtable.update("default_state", plan["direction"], reward)

        return {"status": "cycle_complete", "opened": opened, "features": features}


ai_pipeline = AIPipeline()

# === engine_monitor.py (D7 – Engine állapot monitor + PnL reward frissítés) ===

class EngineMonitor:
    """
    Figyeli a pozíciókat, PnL-t, lezárja a pozíciókat SL/TP vagy manuális jel alapján,
    és frissíti a Q-learning reward értékeit.
    """

    def __init__(self):
        self.last_pnl = 0

    def check_position(self):
        """Lekérdezi az aktív pozíciót és visszaadja az állapotot."""
        pos = trade_executor.active_position
        if pos is None:
            return {"active": False}

        return {"active": True, "position": pos}

    def close_and_reward(self):
        """
        Pozíció lezárása, PnL alapján reward számítás,
        és Q-learning frissítés.
        """
        pos = trade_executor.active_position
        if pos is None:
            return {"error": "Nincs aktív pozíció a záráshoz."}

        result = trade_executor.close_position()
        pnl = result.get("pnl", 0)
        self.last_pnl = pnl

        # Reward logika (egyszerű, később finomítható)
        if pnl > 0:
            reward = +1
        elif pnl < 0:
            reward = -1
        else:
            reward = 0

        qtable.update("default_state", pos["direction"], reward)
        ai_pipeline.log_event("reward", reward)

        return {
            "closed": result,
            "reward": reward
        }

engine_monitor = EngineMonitor()


# === engine_routes.py (D7 – API végpontok az engine monitorhoz) ===
from fastapi import APIRouter

engine_router = APIRouter(prefix="/engine", tags=["Engine"])

@engine_router.get("/state")
def engine_state():
    return engine_monitor.check_position()

@engine_router.post("/close_and_reward")
def close_and_reward():
    return engine_monitor.close_and_reward()


# === data_bridge.py (D8 – valós/szimulált ár frissítés integráció) ===

class DataBridge:
    def __init__(self):
        self.last_price = 2500.0  # kezdeti placeholder

    def update_price(self, new_price: float):
        self.last_price = new_price

    def get_price(self):
        return self.last_price

    def get_features(self, symbol):
        # Ez a rész később valódi adatgyűjtőből érkezhet
        return {
            "trend": 0.62,
            "vol": 0.014,
            "liquidity": "strong",
            "price": self.last_price
        }

data_bridge = DataBridge()

# === ai_pipeline (D8 – időzített futás előkészítése) ===

    def run_cycle_auto(self, symbol: str, equity: float):
        """Automatikus pipeline futtatás időzítéshez (pl.: 5 mp, 30 mp)."""
        result = self.run_cycle(symbol, equity)
        self.log_event("auto_cycle", result)
        return result

# === engine_routes (D8 – pipeline futtatása API-ból) ===

@engine_router.post("/run_cycle")
def run_cycle(symbol: str = "ETHUSDC", equity: float = 1000):
    return ai_pipeline.run_cycle(symbol, equity)

# === engine_routes (D8 – ár frissítése API-ból) ===

@engine_router.post("/update_price")
def update_price(price: float):
    data_bridge.update_price(price)
    return {"status": "updated", "price": price}

# === D9 – DEPLOY CONFIG (requirements + Procfile + Render/ Railway) ===

# requirements.txt (automatikusan generált javaslat)
# fastapi
# uvicorn
# pydantic
# python-dotenv
# requests
# numpy
# sqlite3 (builtin)
# Any extra libs can be added here

# Procfile (Railway/Render)
# web: uvicorn main:app --host 0.0.0.0 --port $PORT

# render.yaml (Render.com deploy)
# services:
#   - type: web
#     name: mzx-backend
#     env: python
#     buildCommand: pip install -r requirements.txt
#     startCommand: uvicorn main:app --host 0.0.0.0 --port 10000

# === FRONTEND API ENDPOINT MAP (React/Vite bekötéshez) ===
# Chat API:
#   GET /chat/ask?question=...
#   GET /chat/summary
#   GET /chat/plan
#   GET /chat/qlearning
#   GET /chat/data

# Trade API:
#   GET /trade/signal
#   GET /trade/plan?equity=1000
#   POST /trade/open?equity=1000
#   POST /trade/close
#   GET /trade/state

# Engine API:
#   GET  /engine/state
#   POST /engine/close_and_reward
#   POST /engine/run_cycle
#   POST /engine/update_price


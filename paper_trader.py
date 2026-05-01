import time
import os
import numpy as np
from dotenv import load_dotenv
from alpaca_trade_api.rest import REST

load_dotenv()

api = REST(
    os.getenv("APCA_API_KEY_ID"),
    os.getenv("APCA_API_SECRET_KEY"),
    os.getenv("APCA_API_BASE_URL")
)

symbols = ["AAPL","MSFT","NVDA","AMZN","META","TSLA","GOOGL"]

THRESHOLD = 0.05
COOLDOWN = 120
MAX_POSITIONS = 5

positions = {}
last_trade_time = {}

def get_bars(symbol):
    try:
        df = api.get_bars(symbol, "5Min", limit=50).df
        if df is None or len(df) < 20:
            return None
        return df
    except Exception as e:
        print("data error", symbol, e)
        return None

def vwap_signal(df):
    vwap = (df["close"] * df["volume"]).cumsum() / (df["volume"].cumsum() + 1e-8)
    dev = (df["close"] - vwap) / (vwap + 1e-8)
    z = (dev - dev.mean()) / (dev.std() + 1e-8)
    return -z.iloc[-1]

def can_trade(symbol):
    if symbol not in last_trade_time:
        return True
    return time.time() - last_trade_time[symbol] > COOLDOWN

def get_equity():
    return float(api.get_account().equity)

def trade(symbol):
    print("processing", symbol)

    df = get_bars(symbol)
    if df is None:
        print("no data", symbol)
        return

    sig = vwap_signal(df)
    price = df["close"].iloc[-1]

    print(symbol, "signal:", round(sig, 4), "price:", round(price, 2))

    if abs(sig) < THRESHOLD:
        return

    if not can_trade(symbol):
        print("cooldown active", symbol)
        return

    if len(positions) >= MAX_POSITIONS and symbol not in positions:
        print("max positions reached")
        return

    equity = get_equity()
    allocation = equity * 0.05
    qty = int(allocation / price)

    if qty <= 0:
        return

    try:
        if sig > 0:
            side = "buy"
            positions[symbol] = "long"
        else:
            side = "sell"
            positions[symbol] = "short"

        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type="market",
            time_in_force="day"
        )

        last_trade_time[symbol] = time.time()

        print("trade executed", symbol, side, qty)

    except Exception as e:
        print("order error", symbol, e)

while True:
    try:
        print("\nEquity:", get_equity(), "| Positions:", len(positions))

        for s in symbols:
            trade(s)

        time.sleep(60)

    except Exception as e:
        print("loop error", e)
        time.sleep(5)
import time
import os
from dotenv import load_dotenv
from alpaca_trade_api.rest import REST
from sp500_universe import load_top_liquid
from vwap_strategy import signal

load_dotenv()

api = REST(
    os.getenv("APCA_API_KEY_ID"),
    os.getenv("APCA_API_SECRET_KEY"),
    os.getenv("APCA_API_BASE_URL")
)

symbols = load_top_liquid()

positions = {}
last_trade_time = {}

COOLDOWN = 300
MAX_POSITIONS = 25


def get_bars(symbol):
    try:
        df = api.get_bars(symbol, "5Min", limit=51).df
        if df is None or len(df) < 40:
            return None
        return df.iloc[:-1]
    except:
        return None


def get_equity():
    return float(api.get_account().equity)


def can_trade(symbol):
    return time.time() - last_trade_time.get(symbol, 0) > COOLDOWN


def trade(symbol):
    df = get_bars(symbol)
    if df is None:
        return

    sig = signal(df)
    price = df["close"].iloc[-1]

    print(f"{symbol} | signal={sig:.2f} | price={price:.2f}")

    if sig == 0:
        return

    if not can_trade(symbol):
        return

    if len(positions) >= MAX_POSITIONS and symbol not in positions:
        return

    equity = get_equity()
    risk_per_trade = equity * 0.001

    qty = risk_per_trade / price
    qty = max(int(qty), 1)

    try:
        if sig > 0:
            api.submit_order(
                symbol=symbol,
                qty=qty,
                side="buy",
                type="market",
                time_in_force="day"
            )
            positions[symbol] = qty
        else:
            api.submit_order(
                symbol=symbol,
                qty=qty,
                side="sell",
                type="market",
                time_in_force="day"
            )
            positions.pop(symbol, None)

        last_trade_time[symbol] = time.time()

    except Exception as e:
        print(symbol, "error", e)


while True:
    print("\nEquity:", get_equity(), "Positions:", len(positions))

    for i, s in enumerate(symbols):
        if i % 5 == 0:
            time.sleep(0.2)
        trade(s)

    time.sleep(60)
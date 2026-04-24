import time
from strategy.screener import screen_universe

def run_bot(exec, universe):
    api = exec.api

    while True:
        try:
            ranked = screen_universe(api, universe)

            for symbol, score in ranked[:3]:
                cash = float(exec.account().cash)

                qty = int((cash * 0.02) / 100)

                if qty > 0:
                    exec.buy(symbol, qty)

            time.sleep(60)

        except Exception as e:
            print("loop error:", e)
            time.sleep(10)
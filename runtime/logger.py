import time

class TradeLogger:
    def __init__(self):
        self.trades = []

    def log(self, symbol, side, qty, price, score):
        self.trades.append({
            "time": time.time(),
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price,
            "score": score
        })

        print(f"{side} {symbol} | qty={qty} | price={price:.2f} | score={score:.3f}")
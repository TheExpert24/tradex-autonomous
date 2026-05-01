import random
from market.orderbook import Order

class MeanReversionStrategy:
    def __init__(self):
        self.window = []

    def on_tick(self, md, broker):
        mid = md["mid"]
        self.window.append(mid)

        if len(self.window) > 20:
            self.window.pop(0)

        avg = sum(self.window) / len(self.window)

        if mid < avg * 0.998:
            broker.send_order(Order(mid + 0.02, 10, "buy", "1", 0))

        elif mid > avg * 1.002:
            broker.send_order(Order(mid - 0.02, 10, "sell", "2", 0))
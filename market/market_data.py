import numpy as np

class MarketData:
    def __init__(self, start_price=100):
        self.price = start_price
        self.vol = 0.02

    def tick(self):
        # microstructure random walk + noise
        shock = np.random.normal(0, self.vol)
        self.price *= (1 + shock)

        bid = self.price - 0.01
        ask = self.price + 0.01

        return {
            "bid": bid,
            "ask": ask,
            "mid": self.price
        }
import numpy as np
from collections import deque

class RealTimeFeatures:
    def __init__(self, window=60):
        self.window = window
        self.prices = deque(maxlen=window)

    def update(self, price):
        self.prices.append(price)

        if len(self.prices) < self.window:
            return None

        arr = np.array(self.prices)

        return {
            "return": (arr[-1] - arr[0]) / arr[0],
            "volatility": np.std(arr),
            "momentum": arr[-1] - arr[-10],
        }
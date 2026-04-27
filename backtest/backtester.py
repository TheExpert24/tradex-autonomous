import numpy as np

class Backtester:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.position = 0
        self.entry_price = 0
        self.history = []

    def step(self, price, signal):
        if signal == 1 and self.position == 0:
            self.position = 1
            self.entry_price = price
            self.cash -= price

        elif signal == -1 and self.position == 1:
            self.position = 0
            self.cash += price

        portfolio_value = self.cash + (self.position * price)
        self.history.append(portfolio_value)

        return portfolio_value

    def run(self, prices, signals):
        for p, s in zip(prices, signals):
            self.step(p, s)

        return np.array(self.history)
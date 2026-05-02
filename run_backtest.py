import numpy as np
import time
from sp500_universe import load_top_liquid
from vwap_strategy import signal
from execution.alpaca_executor import Executor
from data.alpaca_data import DataClient

executor = Executor()
data_client = DataClient(executor.api)

symbols = load_top_liquid()

data = {}

for i, s in enumerate(symbols):
    if i % 5 == 0:
        time.sleep(0.2)

    try:
        df = data_client.get_bars(s)
        if df is None or len(df) < 100:
            continue
        data[s] = df
    except:
        continue

symbols = list(data.keys())

class Portfolio:
    def __init__(self, cash=10000):
        self.cash = cash
        self.positions = {}
        self.entry = {}
        self.trades = []

    def value(self, prices):
        total = self.cash
        for s, q in self.positions.items():
            total += q * prices.get(s, 0)
        return total

    def buy(self, s, price, qty):
        cost = price * qty
        if cost > self.cash:
            qty = self.cash / price
            cost = price * qty
        self.cash -= cost
        self.positions[s] = self.positions.get(s, 0) + qty
        self.entry[s] = price
        self.trades.append(("BUY", s, price, qty))

    def sell(self, s, price):
        if s not in self.positions:
            return
        qty = self.positions[s]
        entry = self.entry.get(s, price)
        pnl = (price - entry) * qty
        self.cash += qty * price
        self.trades.append(("SELL", s, price, qty, pnl))
        del self.positions[s]
        del self.entry[s]


portfolio = Portfolio()
equity_curve = []

length = min(len(data[s]) for s in symbols)

for i in range(50, length):

    prices = {}
    scores = []

    for s in symbols:
        df = data[s]
        price = float(df["close"].iloc[i])
        prices[s] = price

        sig = signal(df)
        scores.append((s, abs(sig), sig, price))

    scores.sort(key=lambda x: x[1], reverse=True)
    top = scores[:40]

    for s, _, sig, price in top:
        qty = (portfolio.cash * 0.001) / price

        if sig > 0:
            portfolio.buy(s, price, qty)
        elif sig < 0:
            portfolio.sell(s, price)

    equity_curve.append(portfolio.value(prices))


eq = np.array(equity_curve)
rets = np.diff(eq) / (eq[:-1] + 1e-9)

total_return = (eq[-1] - eq[0]) / eq[0]

peak = eq[0]
max_dd = 0

for x in eq:
    peak = max(peak, x)
    max_dd = max(max_dd, (peak - x) / peak)

sharpe = np.mean(rets) / (np.std(rets) + 1e-9) * np.sqrt(252)

print("RETURN", total_return)
print("MAX_DD", max_dd)
print("SHARPE", sharpe)
print("TRADES", len(portfolio.trades))
print("FINAL", eq[-1])
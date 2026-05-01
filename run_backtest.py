import numpy as np
import pandas as pd


class MomentumStrategy:
    def __init__(self, lookback=20):
        self.lookback = lookback

    def generate(self, data, i):
        if i < self.lookback:
            return 0

        prices = data["close"].iloc[i - self.lookback:i]

        momentum = np.log(prices.iloc[-1] / prices.iloc[0])
        slope = np.polyfit(np.arange(len(prices)), prices.values, 1)[0]

        rets = prices.pct_change().dropna()
        vol = np.std(rets)

        if np.isnan(vol) or vol == 0 or vol < 0.001:
            return 0

        if momentum > 0 and slope > 0:
            return 1
        if momentum < 0 and slope < 0:
            return -1

        return 0


class Portfolio:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.position = 0.0
        self.entry_price = None
        self.trades = []

    def mark_to_market(self, price):
        return self.cash + self.position * price

    def buy(self, price, size):
        cost = price * size
        if cost > self.cash:
            size = self.cash / price
            cost = price * size

        self.cash -= cost
        self.position += size
        self.entry_price = price

        self.trades.append({"type": "BUY", "price": price, "size": size})

    def sell(self, price):
        if self.position == 0:
            return

        pnl = (price - self.entry_price) * self.position
        self.cash += self.position * price

        self.trades.append({"type": "SELL", "price": price, "size": self.position, "pnl": pnl})

        self.position = 0
        self.entry_price = None


class Backtester:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy
        self.portfolio = Portfolio()
        self.equity_curve = []

    def run(self):
        for i in range(len(self.data)):
            price = float(self.data["close"].iloc[i])
            signal = self.strategy.generate(self.data, i)

            size = (self.portfolio.cash * 0.1) / price

            if signal == 1 and self.portfolio.position == 0:
                self.portfolio.buy(price, size)
            elif signal == -1 and self.portfolio.position > 0:
                self.portfolio.sell(price)

            self.equity_curve.append(self.portfolio.mark_to_market(price))

        return self.report()

    def report(self):
        equity = np.array(self.equity_curve)
        returns = np.diff(equity) / (equity[:-1] + 1e-9)

        total_return = (equity[-1] - equity[0]) / equity[0]

        peak = equity[0]
        max_dd = 0
        for e in equity:
            peak = max(peak, e)
            max_dd = max(max_dd, (peak - e) / peak)

        sharpe = np.mean(returns) / (np.std(returns) + 1e-9) * np.sqrt(252)

        trades = self.portfolio.trades
        wins = [t["pnl"] for t in trades if t.get("pnl", 0) > 0]
        losses = [t["pnl"] for t in trades if t.get("pnl", 0) < 0]

        win_rate = len(wins) / max(len(wins) + len(losses), 1)
        profit_factor = sum(wins) / abs(sum(losses)) if losses else float("inf")

        print("\n--- INSTITUTIONAL REPORT ---")
        print(f"Total Return: {total_return:.4f}")
        print(f"Max Drawdown: {max_dd:.4f}")
        print(f"Sharpe Ratio: {sharpe:.4f}")
        print(f"Win Rate: {win_rate:.4f}")
        print(f"Profit Factor: {profit_factor:.4f}")
        print(f"Trades: {len(trades)}")

        return equity[-1]


class Simulator:
    def __init__(self, data):
        self.engine = Backtester(data, MomentumStrategy())

    def run(self):
        return self.engine.run()


if __name__ == "__main__":
    data = pd.DataFrame({"close": 100 + np.cumsum(np.random.randn(1000))})
    sim = Simulator(data)
    final_equity = sim.run()
    print(f"\nfinal equity: {final_equity}")
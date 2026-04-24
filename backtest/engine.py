import numpy as np

from backtest.portfolio import Portfolio
from backtest.metrics import max_drawdown, sharpe

from data.feature_engine import build_features
from data.labels import create_labels
from models.train import make_sequences

class Backtester:
    def __init__(self, model, data, window=30):
        self.model = model
        self.data = data
        self.window = window

    def run(self, symbols):

        portfolio = Portfolio()
        equity = []

        for t in range(100, len(self.data[symbols[0]])):

            prices = {}
            dataset = {}

            for s in symbols:
                df = self.data[s].iloc[:t]

                if len(df) < self.window:
                    continue

                df = build_features(df)
                dataset[s] = df
                prices[s] = df["close"].iloc[-1]

            if not dataset:
                continue

            signals = {}

            for s, df in dataset.items():
                X, _ = make_sequences(df, self.window)

                if len(X) == 0:
                    continue

                x = X[-1:]
                pred = self.model.forward(x)[0]

                signals[s] = float(pred)

            ranked = sorted(signals.items(), key=lambda x: x[1], reverse=True)[:5]

            for sym, score in ranked:

                price = prices[sym]

                if score > 0.65:
                    portfolio.buy(sym, 10, price)

                elif score < 0.35:
                    if sym in portfolio.positions:
                        portfolio.sell(sym, portfolio.positions[sym]["qty"], price)

            value = portfolio.value(prices)
            equity.append(value)

        rets = np.diff(equity) / equity[:-1]

        return {
            "final_value": equity[-1],
            "max_drawdown": max_drawdown(equity),
            "sharpe": sharpe(rets),
            "equity_curve": equity
        }
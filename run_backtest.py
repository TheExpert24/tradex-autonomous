import numpy as np

from execution.alpaca_executor import Executor
from data.alpaca_data import DataClient
from data.feature_engine import build_features
from models.lstm_model import LSTMModel
from models.train import make_sequences
from config.features import FEATURE_COLUMNS

WINDOW = 30

executor = Executor()
data = DataClient(executor.api)

symbols = [
    "AAPL","MSFT","NVDA","AMZN","GOOGL","META","TSLA",
    "UNH","XOM","JPM","V","PG","MA","HD","CVX",
    "ABBV","LLY","KO","PEP","COST","AVGO","MRK","WMT",
    "BAC","ADBE","CRM","NFLX","ACN","MCD","DHR","LIN",
    "NEE","AMD","INTC","QCOM","TXN","HON","PM","ORCL",
    "UNP","LOW","UPS","GS","MS","RTX","CAT","IBM","GE"
]

model = LSTMModel(WINDOW, features=len(FEATURE_COLUMNS))
model.load("models/lstm_model.pth")

all_preds = []
all_returns = []

for s in symbols:
    try:
        df = data.get_bars(s)

        if df is None or len(df) < WINDOW + 50:
            continue

        df = build_features(df)
        close = df["close"].values

        df = df[FEATURE_COLUMNS]
        df = (df - df.mean()) / (df.std() + 1e-8)

        X, _ = make_sequences(df, WINDOW)

        if len(X) < 10:
            continue

        preds = model.predict(X).flatten()

        future_ret = (close[WINDOW+1:] - close[WINDOW:-1]) / close[WINDOW:-1]

        min_len = min(len(preds), len(future_ret))

        preds = preds[:min_len]
        future_ret = future_ret[:min_len]

        all_preds.append(preds)
        all_returns.append(future_ret)

    except Exception as e:
        print("ERROR:", s, e)

min_len = min(len(x) for x in all_preds)

preds_matrix = np.array([x[-min_len:] for x in all_preds])
returns_matrix = np.array([x[-min_len:] for x in all_returns])

capital = 10000
fee = 0.0003

for t in range(min_len - 1):

    preds_t = preds_matrix[:, t]
    rets_t = returns_matrix[:, t]

    ranks = np.argsort(preds_t)

    long_idx = ranks[-5:]
    short_idx = ranks[:5]

    long_ret = np.mean(rets_t[long_idx])
    short_ret = np.mean(rets_t[short_idx])

    pnl = 0.5 * long_ret - 0.5 * short_ret

    capital *= (1 + pnl - fee)

print("Final Portfolio Value:", capital)
print("Return:", (capital / 10000 - 1) * 100, "%")
print("Trades executed:", min_len)
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

X_all, y_all = [], []

for s in symbols:
    try:
        df = data.get_bars(s)
        if df is None or len(df) < 150:
            continue

        df = build_features(df)
        df = df[FEATURE_COLUMNS]

        df = (df - df.mean()) / (df.std() + 1e-8)

        close = df["close"].values

        future_ret = np.roll(close, -5) / close - 1

        df = df.iloc[:-5]
        future_ret = future_ret[:-5]

        X, _ = make_sequences(df, WINDOW)
        y = future_ret[WINDOW:]

        mask = np.isfinite(y)

        X = X[mask]
        y = y[mask]

        if len(X) < 30:
            continue

        X_all.append(X)
        y_all.append(y)

    except:
        continue

X_all = np.vstack(X_all)
y_all = np.hstack(y_all)

y_all = np.argsort(np.argsort(y_all))
y_all = y_all / len(y_all)

model = LSTMModel(WINDOW, features=len(FEATURE_COLUMNS))
model.fit(X_all, y_all, epochs=5)

model.save("models/lstm_model.pth")

print("Model trained.")
import numpy as np

from execution.alpaca_executor import Executor
from data.alpaca_data import DataClient
from data.feature_engine import build_features
from data.labels import create_labels

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

print("Universe size:", len(symbols))

X_all, y_all = [], []

for s in symbols:
    try:
        df = data.get_bars(s)

        if df is None or len(df) < 100:
            continue

        df = build_features(df)

        if len(df) < WINDOW + 10:
            continue

        df = df[FEATURE_COLUMNS]

        labels = create_labels(df, horizon=5)

        df = df.iloc[:-5]
        labels = labels[:-5]

        X, _ = make_sequences(df, WINDOW)

        y = labels[WINDOW:].values

        mask = ~np.isnan(y)

        X = X[mask]
        y = y[mask]

        if len(X) < 10:
            continue

        X_all.append(X)
        y_all.append(y)

        print("OK:", s, len(X))

    except Exception as e:
        print("ERROR:", s, e)

if len(X_all) == 0:
    raise Exception("No valid training data produced")

X_all = np.vstack(X_all)
y_all = np.hstack(y_all)

print("\nFinal dataset shape:", X_all.shape, y_all.shape)

model = LSTMModel(WINDOW, features=len(FEATURE_COLUMNS))
model.fit(X_all, y_all, epochs=5)

model.save("models/lstm_model.pth")

print("\nModel trained and saved.")
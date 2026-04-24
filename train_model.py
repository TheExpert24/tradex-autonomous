import numpy as np

from execution.alpaca_executor import Executor
from universe.universe import Universe
from universe.filter import filter_universe

from data.alpaca_data import DataClient
from data.feature_engine import build_features

from models.lstm_model import LSTMModel
from models.train import make_sequences

WINDOW = 30

data = DataClient()

exec = Executor()
universe = Universe(exec.api)

raw_symbols = universe.get_all_symbols()
symbols = raw_symbols[:300]

print("Universe size:", len(symbols))

X_all, y_all = [], []

for s in symbols:
    print("\nSymbol:", s)

    try:
        df = data.get_bars(s)

        if df is None or len(df) < 20:
            continue

        df = build_features(df)

        if len(df) < WINDOW:
            continue

        X, y = make_sequences(df, WINDOW)

        if len(X) < 5:
            continue

        X_all.append(X)
        y_all.append(y)

    except Exception as e:
        print("Error:", s, e)
        continue

print("\nX_all sizes:", [len(x) for x in X_all])
print("Symbols used:", len(X_all))

if len(X_all) == 0:
    raise Exception("No training data")

X_all = np.vstack(X_all)
y_all = np.hstack(y_all)

print("Final dataset shape:", X_all.shape, y_all.shape)

FEATURES = X_all.shape[2]

model = LSTMModel(WINDOW, FEATURES)
model.train(X_all, y_all, epochs=5)

model.save("models/latest_model.pt")

print("\nModel trained and saved.")
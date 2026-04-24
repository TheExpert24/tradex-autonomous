import numpy as np

from execution.alpaca_executor import Executor
from data.alpaca_data import DataClient
from data.feature_engine import build_features
from data.labels import create_labels

from models.lstm_model import LSTMModel
from models.train import make_sequences

from sklearn.utils import resample

WINDOW = 30

executor = Executor()
data = DataClient(executor.api)

symbols = [
    "AAPL","MSFT","NVDA","AMZN","GOOGL","META","TSLA",
    "BRK-B","UNH","XOM","JPM","V","PG","MA","HD",
    "CVX","ABBV","LLY","KO","PEP","COST","AVGO",
    "MRK","WMT","BAC","ADBE","CRM","NFLX","ACN",
    "MCD","DHR","LIN","NEE","AMD","INTC","QCOM",
    "TXN","HON","PM","ORCL","UNP","LOW","UPS",
    "GS","MS","RTX","CAT","IBM","GE"
]

def normalize(df):
    df = df.copy()
    for c in df.columns:
        df[c] = (df[c] - df[c].mean()) / (df[c].std() + 1e-8)
    return df

def balance(X, y):
    X0 = X[y == 0]
    X1 = X[y == 1]

    if len(X0) == 0 or len(X1) == 0:
        return X, y

    n = min(len(X0), len(X1))

    X0 = resample(X0, n_samples=n, random_state=42)
    X1 = resample(X1, n_samples=n, random_state=42)

    Xb = np.vstack([X0, X1])
    yb = np.hstack([np.zeros(n), np.ones(n)])

    return Xb, yb


print("Universe size:", len(symbols))

X_all, y_all = [], []
used = 0

for s in symbols:
    try:
        symbol = s.replace(".", "-")

        df = data.get_bars(symbol)

        if df is None or len(df) < 100:
            print("SKIP DATA:", symbol)
            continue

        df = build_features(df)

        if df is None or len(df) == 0:
            print("FAIL FEATURES:", symbol)
            continue

        df = df.select_dtypes(include=[np.number])

        if len(df.columns) == 0:
            print("NO NUMERIC FEATURES:", symbol)
            continue

        if len(df) < WINDOW + 10:
            print("TOO SHORT:", symbol)
            continue

        df = normalize(df)

        labels = create_labels(df, horizon=10, threshold=0.002)

        if labels is None or len(labels) == 0:
            print("FAIL LABELS:", symbol)
            continue

        df = df.iloc[:-10]
        labels = labels[:-10]

        X, y = make_sequences(df, WINDOW)

        if X is None or len(X) == 0:
            print("NO SEQUENCES:", symbol)
            continue

        if len(y) != len(X):
            y = y[:len(X)]

        y = np.array(y)

        mask = ~np.isnan(y)

        if mask.sum() == 0:
            print("ALL LABELS NAN:", symbol)
            continue

        X = X[mask]
        y = y[mask]

        if len(X) < 10:
            print("TOO SMALL:", symbol)
            continue

        X_all.append(X)
        y_all.append(y)

        used += 1
        print("OK:", symbol, len(X))

    except Exception as e:
        print("ERROR:", symbol, e)
        continue

if len(X_all) == 0:
    raise Exception("No valid training data produced")

X_all = np.vstack(X_all)
y_all = np.hstack(y_all)

if len(X_all.shape) == 2:
    X_all = X_all.reshape(X_all.shape[0], X_all.shape[1], 1)

X_all, y_all = balance(X_all, y_all)

print("\nFinal dataset shape:", X_all.shape, y_all.shape)
print("Symbols used:", used)

FEATURES = X_all.shape[2]

model = LSTMModel(WINDOW, FEATURES)
model.train(X_all, y_all, epochs=5)

model.save("models/lstm_model.pth")

print("\nModel trained and saved.")
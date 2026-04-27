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

capital = 10000
trades = 0

for symbol in symbols:
    try:
        df = data.get_bars(symbol)

        if df is None or len(df) < WINDOW + 50:
            continue

        df = build_features(df)

        if len(df) == 0:
            continue

        close = df["close"].values

        df = df[FEATURE_COLUMNS]

        X, _ = make_sequences(df, WINDOW)

        if len(X) == 0:
            continue

        preds = model.predict(X)

        prices = close[-len(preds):]

        for i in range(len(preds) - 1):
            signal = preds[i]

            position = np.tanh(signal * 10)

            ret = (prices[i+1] - prices[i]) / prices[i]

            capital *= (1 + position * ret)

            trades += 1

    except Exception as e:
        print("ERROR:", symbol, e)

print("Final Portfolio Value:", capital)
print("Return:", (capital / 10000 - 1) * 100, "%")
print("Trades executed:", trades)
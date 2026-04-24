import time
import numpy as np

from data.alpaca_data import DataClient
from data.feature_engine import build_features
from universe.universe import Universe

from models.lstm_model import LSTMModel
from models.train import make_sequences
from signals.signal_generator import SignalGenerator

from risk.risk_manager import RiskManager
from execution.alpaca_executor import Executor
from config.config import *

data = DataClient()
exec = Executor()
risk = RiskManager()

universe = Universe(exec.api)

START_EQUITY = float(exec.account().equity)

WINDOW = 30
TOP_K = 5

raw_symbols = universe.get_all_symbols()

if not raw_symbols:
    raise Exception("Universe empty")

symbols = raw_symbols[:200]

X_all, y_all = [], []
valid_symbols = []

for s in symbols:
    try:
        df = data.get_bars(s)

        if df is None or len(df) < 120:
            continue

        df = build_features(df)

        if len(df) < WINDOW:
            continue

        X, y = make_sequences(df, WINDOW)

        if len(X) == 0:
            continue

        X_all.append(X)
        y_all.append(y)
        valid_symbols.append(s)

    except:
        continue

if len(X_all) == 0:
    raise Exception("No training data built")

X_all = np.vstack(X_all)
y_all = np.hstack(y_all)

FEATURES = X_all.shape[2]

model = LSTMModel(WINDOW, FEATURES)
model.train(X_all, y_all, epochs=5)

signal_engine = SignalGenerator(model)

while True:
    dataset = {}

    for s in valid_symbols:
        try:
            df = data.get_bars(s)

            if df is None or len(df) < WINDOW:
                continue

            df = build_features(df)

            dataset[s] = df

        except:
            continue

    ranked = signal_engine.rank(dataset)[:TOP_K]

    account = exec.account()
    equity = float(account.equity)

    positions = exec.api.list_positions()

    if risk.check_drawdown(START_EQUITY, equity):
        break

    if not risk.can_open_new_position(positions):
        time.sleep(300)
        continue

    for symbol, score in ranked:
        if score < 0.65:
            continue

        if symbol in [p.symbol for p in positions]:
            continue

        try:
            price = dataset[symbol]["close"].iloc[-1]
            qty = risk.position_size(equity, price)

            if qty <= 0:
                continue

            exec.buy(symbol, qty)

        except:
            continue

    time.sleep(300)
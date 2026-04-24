import numpy as np

def create_labels(df, horizon=10, threshold=0.002):
    future = df["close"].shift(-horizon)
    returns = (future - df["close"]) / df["close"]

    y = np.full(len(df), np.nan)

    y[returns > threshold] = 1
    y[returns < -threshold] = 0

    return y
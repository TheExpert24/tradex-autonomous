import numpy as np

def compute_vwap(df):
    return (df["close"] * df["volume"]).cumsum() / (df["volume"].cumsum() + 1e-8)

def signal(df):
    vwap = compute_vwap(df)
    dev = (df["close"] - vwap) / (vwap + 1e-8)

    mean = np.mean(dev)
    std = np.std(dev) + 1e-8
    z = (dev - mean) / std

    return -z.iloc[-1]
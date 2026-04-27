import numpy as np
import pandas as pd

def build_features(df):
    df = df.copy()

    df["return"] = df["close"].pct_change()

    df["ma_5"] = df["close"].rolling(5).mean()
    df["ma_10"] = df["close"].rolling(10).mean()
    df["ma_20"] = df["close"].rolling(20).mean()

    df["volatility"] = df["return"].rolling(10).std()

    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / (loss + 1e-9)
    df["rsi"] = 100 - (100 / (1 + rs))

    df["momentum"] = df["close"] - df["close"].shift(10)

    df = df.dropna()

    return df
import pandas as pd

def build_features(df):
    df = df.copy()

    df["return"] = df["close"].pct_change()
    df["ma5"] = df["close"].rolling(5).mean()
    df["ma10"] = df["close"].rolling(10).mean()
    df["volatility"] = df["return"].rolling(5).std()
    df["volume_avg"] = df["volume"].rolling(5).mean()

    df = df.fillna(0)

    return df
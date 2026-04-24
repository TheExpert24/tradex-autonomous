import numpy as np

def build_features(df):
    df = df.copy()

    if "close" not in df.columns:
        return None

    df["return"] = df["close"].pct_change()
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    df["high_low"] = (df["high"] - df["low"]) / df["close"]
    df["open_close"] = (df["close"] - df["open"]) / df["open"]
    df["volume_change"] = df["volume"].pct_change()

    df = df.dropna()

    return df
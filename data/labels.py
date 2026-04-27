def create_labels(df, horizon=5):
    returns = df["close"].shift(-horizon) / df["close"] - 1
    return returns
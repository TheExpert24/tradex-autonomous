import numpy as np

def score_symbol(df):
    if df is None or len(df) < 5:
        return None

    returns = df["close"].pct_change().fillna(0)

    momentum = returns.tail(3).mean()
    volatility = returns.std()
    volume = df["volume"].mean()

    score = (momentum * 2.0) - (volatility * 1.5) + (volume / 1e6)

    return score
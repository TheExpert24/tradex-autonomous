import numpy as np

def build_factors(df, spy_df):
    df = df.copy()

    ret = df["close"].pct_change()
    spy_ret = spy_df["close"].pct_change()

    excess = ret - spy_ret

    df["alpha_momentum"] = excess.rolling(12).sum()
    df["alpha_reversal"] = -excess.rolling(3).mean()
    df["volatility"] = ret.rolling(20).std()
    df["volume_signal"] = df["volume"] / (df["volume"].rolling(20).mean() + 1e-8)

    df = df.dropna()
    return df
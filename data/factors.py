import numpy as np

def build_factors(df, spy, sector):
    df = df.copy()

    r = df["close"].pct_change()
    spy_r = spy["close"].pct_change()
    sector_r = sector["close"].pct_change()

    rel_market = r - spy_r
    rel_sector = r - sector_r

    macro_trend = spy_r.rolling(20).mean()
    macro_vol = spy_r.rolling(20).std()

    sentiment_proxy = (rel_sector.rolling(5).mean() - rel_market.rolling(5).mean())

    df["momentum"] = rel_market.rolling(12).mean()
    df["reversal"] = -rel_market.rolling(3).mean()
    df["sector_strength"] = rel_sector.rolling(12).mean()

    df["macro_trend"] = macro_trend
    df["macro_vol"] = macro_vol
    df["sentiment"] = sentiment_proxy

    df["volatility"] = r.rolling(20).std()
    df["volume_signal"] = df["volume"] / (df["volume"].rolling(20).mean() + 1e-8)

    return df.dropna()
import numpy as np

def signal(df):
    if len(df) < 40:
        return 0

    close = df["close"]
    volume = df["volume"]

    returns = close.pct_change()
    vol = returns.std()

    if np.isnan(vol):
        return 0

    vwap = (close * volume).cumsum() / (volume.cumsum() + 1e-8)
    dev = (close - vwap) / (vwap + 1e-8)
    z = (dev - dev.mean()) / (dev.std() + 1e-8)

    vwap_signal = -z.iloc[-1]

    mom_10 = close.iloc[-1] / close.iloc[-10] - 1
    mom_20 = close.iloc[-1] / close.iloc[-20] - 1

    momentum = 0.6 * mom_10 + 0.4 * mom_20

    trend_slope = np.polyfit(np.arange(30), close.iloc[-30:], 1)[0]
    trend_strength = abs(trend_slope) / (close.iloc[-1] + 1e-8)

    trend_regime = abs(momentum) + trend_strength
    is_trending = trend_regime > 0.01

    if is_trending:
        alpha = 0.60 * momentum + 0.30 * trend_slope + 0.10 * vwap_signal
    else:
        alpha = 0.60 * vwap_signal + 0.30 * momentum + 0.10 * trend_slope

    alpha = alpha * (1 - min(vol * 40, 1.0))

    if abs(alpha) < 0.12:
        return 0

    return 1 if alpha > 0 else -1
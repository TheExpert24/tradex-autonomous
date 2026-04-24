import numpy as np

def max_drawdown(equity):
    peak = equity[0]
    max_dd = 0

    for x in equity:
        peak = max(peak, x)
        dd = (peak - x) / peak
        max_dd = max(max_dd, dd)

    return max_dd


def sharpe(returns):
    if len(returns) < 2:
        return 0

    return np.mean(returns) / (np.std(returns) + 1e-9) * np.sqrt(252)
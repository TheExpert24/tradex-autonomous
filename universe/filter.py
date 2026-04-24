import time

def filter_universe(api, symbols, max_symbols=200):
    filtered = []

    symbols = symbols[:max_symbols]

    for i, s in enumerate(symbols):
        try:
            bars = api.get_bars(s, "1Day", limit=5).df

            if bars is None or len(bars) < 3:
                continue

            if bars.index.nunique() < 2:
                continue

            if "volume" not in bars.columns:
                continue

            avg_vol = bars["volume"].mean()

            if avg_vol > 20000:
                filtered.append(s)

        except:
            continue

        if i % 10 == 0:
            time.sleep(0.2)

    return filtered
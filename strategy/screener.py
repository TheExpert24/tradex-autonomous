from strategy.scorer import score_symbol

def screen_universe(api, symbols):
    scored = []

    for s in symbols:
        try:
            df = api.get_bars(s, "1Day", limit=10).df

            score = score_symbol(df)

            if score is not None:
                scored.append((s, score))

        except:
            continue

    scored.sort(key=lambda x: x[1], reverse=True)

    return scored[:10]
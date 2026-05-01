import numpy as np

from execution.alpaca_executor import Executor
from data.alpaca_data import DataClient
from data.factors import build_factors
from models.score_model import ScoreModel

executor = Executor()
data = DataClient(executor.api)

symbols = [
    "AAPL","MSFT","NVDA","AMZN","GOOGL","META","TSLA",
    "UNH","XOM","JPM","V","PG","MA","HD","CVX",
    "ABBV","LLY","KO","PEP","COST","AVGO","MRK","WMT",
    "BAC","ADBE","CRM","NFLX","ACN","MCD","DHR","LIN",
    "NEE","AMD","INTC","QCOM","TXN","HON","PM","ORCL",
    "UNP","LOW","UPS","GS","MS","RTX","CAT","IBM","GE"
]

spy = data.get_bars("SPY")

def regime_filter(spy):
    r = spy["close"].pct_change()
    vol = r.rolling(20).std().iloc[-1]
    trend = r.rolling(20).mean().iloc[-1]

    if np.isnan(vol) or np.isnan(trend):
        return False

    if vol > 0.02:
        return False

    if abs(trend) < 0.0003:
        return False

    return True

model = ScoreModel()

all_scores = []
all_returns = []
all_vol = []

for s in symbols:
    try:
        df = data.get_bars(s)

        if df is None or len(df) < 150:
            continue

        df = build_factors(df, spy)

        close = df["close"].values
        spy_close = spy["close"].values[:len(close)]

        future_ret = (np.roll(close, -10) / close) - 1
        spy_ret = (np.roll(spy_close, -10) / spy_close) - 1

        alpha = future_ret - spy_ret

        df = df[:-10]
        alpha = alpha[:-10]

        scores = model.score(df)

        vol = np.std(df["close"].pct_change().fillna(0).values) + 1e-8

        m = min(len(scores), len(alpha))

        all_scores.append(scores[:m])
        all_returns.append(alpha[:m])
        all_vol.append(vol)

    except:
        continue

if len(all_scores) == 0:
    raise Exception("No valid data collected.")

min_len = min(len(x) for x in all_scores)

scores_matrix = np.array([x[-min_len:] for x in all_scores])
returns_matrix = np.array([x[-min_len:] for x in all_returns])
vol_vector = np.array(all_vol)

capital = 10000
fee = 0.0003

position = np.zeros(len(symbols))
alpha_decay = 0.85

for t in range(min_len):

    if not regime_filter(spy):
        continue

    scores_t = scores_matrix[:, t]
    rets_t = returns_matrix[:, t]

    z = (scores_t - np.mean(scores_t)) / (np.std(scores_t) + 1e-8)

    raw_weights = z.copy()

    raw_weights = raw_weights / (np.sum(np.abs(raw_weights)) + 1e-8)

    vol_adj = 1 / vol_vector
    vol_adj = vol_adj / np.sum(vol_adj)

    target = raw_weights * vol_adj

    position = alpha_decay * position + (1 - alpha_decay) * target

    pnl = np.sum(position * rets_t)

    turnover = np.sum(np.abs(position - target))

    capital *= (1 + pnl - fee * turnover)

print("Final Portfolio Value:", capital)
print("Return %:", (capital / 10000 - 1) * 100)
print("Trades:", min_len)
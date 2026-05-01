import numpy as np

class ScoreModel:
    def __init__(self):
        self.w = {
            "momentum": 0.25,
            "reversal": 0.15,
            "sector_strength": 0.20,
            "sentiment": 0.25,
            "macro_trend": 0.15,
            "volume_signal": 0.05,
            "volatility": -0.2
        }

    def score(self, df):
        s = np.zeros(len(df))

        for k, w in self.w.items():
            x = df[k].values
            x = (x - np.mean(x)) / (np.std(x) + 1e-8)
            s += w * x

        return s
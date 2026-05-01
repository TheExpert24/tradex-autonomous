import numpy as np

class ScoreModel:
    def __init__(self):
        self.weights = {
            "momentum_12_1": 0.45,
            "mean_reversion_5": 0.25,
            "volume_signal": 0.15,
            "volatility": -0.25
        }

    def score(self, df):
        score = np.zeros(len(df))

        for f, w in self.weights.items():
            if f in df.columns:
                x = df[f].values
                x = (x - np.mean(x)) / (np.std(x) + 1e-8)
                score += w * x

        return score
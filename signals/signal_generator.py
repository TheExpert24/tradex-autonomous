import numpy as np

class SignalGenerator:
    def __init__(self, model):
        self.model = model

    def rank(self, dataset):
        scores = []

        for symbol, df in dataset.items():
            try:
                X = df.values

                # take last WINDOW slice
                window = 30
                if len(X) < window:
                    continue

                x_input = X[-window:]
                x_input = np.expand_dims(x_input, axis=0)

                pred = self.model.predict(x_input)

                score = float(pred)

                scores.append((symbol, score))

            except:
                continue

        # sort best signals first
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
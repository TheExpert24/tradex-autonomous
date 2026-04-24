import numpy as np

def make_sequences(df, window):
    features = df.select_dtypes(include=[np.number]).values

    X, y = [], []

    for i in range(len(features) - window - 1):
        X.append(features[i:i+window])
        y.append(1 if features[i+window][0] > features[i+window-1][0] else 0)

    return np.array(X), np.array(y)
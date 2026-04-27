import numpy as np

def make_sequences(df, window):
    X = []
    y = []

    values = df.values

    for i in range(len(values) - window):
        X.append(values[i:i+window])
        y.append(values[i+window][-1])

    return np.array(X), np.array(y)
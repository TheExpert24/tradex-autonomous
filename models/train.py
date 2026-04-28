import numpy as np

def make_sequences(df, window):
    X = []
    for i in range(len(df) - window):
        X.append(df.iloc[i:i+window].values)
    return np.array(X), None
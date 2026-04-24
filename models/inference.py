def predict(model, features):
    import numpy as np

    X = np.array(list(features.values())).reshape(1, -1)
    return model.predict(X)[0]
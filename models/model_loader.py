import torch

class ModelLoader:
    def __init__(self, path):
        self.model = torch.load(path)
        self.model.eval()

    def predict(self, x):
        with torch.no_grad():
            return self.model(x)
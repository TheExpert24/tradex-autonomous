import torch
import torch.nn as nn

class LSTMModel(nn.Module):
    def __init__(self, window, features):
        super().__init__()
        self.lstm = nn.LSTM(features, 64, batch_first=True)
        self.fc = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.fc(out)
        return self.sigmoid(out).squeeze()

    def train(self, X, y, epochs=5):
        X = torch.tensor(X, dtype=torch.float32)
        y = torch.tensor(y, dtype=torch.float32)

        opt = torch.optim.Adam(self.parameters(), lr=0.001)
        loss_fn = nn.BCELoss()

        for i in range(epochs):
            opt.zero_grad()
            preds = self.forward(X)
            loss = loss_fn(preds, y)
            loss.backward()
            opt.step()

            print(f"Epoch {i+1}/{epochs} Loss: {loss.item():.4f}")

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path):
        self.load_state_dict(torch.load(path))
        self.eval()
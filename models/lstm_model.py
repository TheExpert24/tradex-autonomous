import torch
import torch.nn as nn
import torch.optim as optim

class LSTMModel(nn.Module):
    def __init__(self, window, features, hidden=64):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=features,
            hidden_size=hidden,
            batch_first=True
        )

        self.fc = nn.Linear(hidden, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.fc(out)
        return self.sigmoid(out)

    def train(self, X, y, epochs=5, lr=0.001):
        X = torch.tensor(X, dtype=torch.float32)
        y = torch.tensor(y, dtype=torch.float32).view(-1, 1)

        optimizer = optim.Adam(self.parameters(), lr=lr)
        loss_fn = nn.BCELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()

            preds = self.forward(X)
            loss = loss_fn(preds, y)

            loss.backward()
            optimizer.step()

            print(f"Epoch {epoch+1}/{epochs} Loss: {loss.item():.4f}")

    def save(self, path):
        torch.save(self, path)

    @staticmethod
    def load(path):
        return torch.load(path)
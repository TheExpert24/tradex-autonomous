import torch
import torch.nn as nn
import torch.optim as optim

class LSTMModel(nn.Module):
    def __init__(self, window, features):
        super().__init__()
        self.lstm = nn.LSTM(features, 64, batch_first=True)
        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        return self.fc(out)

    def fit(self, X, y, epochs=5, lr=0.001):
        self.train()

        X = torch.tensor(X, dtype=torch.float32)
        y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)

        optimizer = optim.Adam(self.parameters(), lr=lr)
        loss_fn = nn.MSELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self(X)
            loss = loss_fn(outputs, y)
            loss.backward()
            optimizer.step()

            print(f"Epoch {epoch+1}/{epochs} Loss: {loss.item():.6f}")

    def predict(self, X):
        self.eval()
        with torch.no_grad():
            X = torch.tensor(X, dtype=torch.float32)
            return self(X).numpy().flatten()

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path):
        self.load_state_dict(torch.load(path))
        self.eval()
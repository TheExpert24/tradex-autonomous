from execution.alpaca_executor import Executor
from universe.universe import Universe
from data.alpaca_data import DataClient
from models.lstm_model import LSTMModel
from backtest.engine import Backtester

exec = Executor()
data = DataClient()

universe = Universe(exec.api)

symbols = universe.get_all_symbols()[:50]

print("Backtesting symbols:", len(symbols))

history = {}

for s in symbols:
    df = data.get_bars(s)
    if df is not None:
        history[s] = df

model = LSTMModel(30, 12)
model.load("models/lstm_model.pth")

bt = Backtester(model, history)

results = bt.run(symbols)

print("\nRESULTS")
print("Final Value:", results["final_value"])
print("Max Drawdown:", results["max_drawdown"])
print("Sharpe:", results["sharpe"])
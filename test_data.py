from execution.alpaca_executor import Executor
from data.alpaca_data import DataClient

exec = Executor()
data = DataClient(exec.api)

df = data.get_bars("AAPL")

print(df.head())
print(len(df))
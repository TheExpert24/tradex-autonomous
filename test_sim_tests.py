from run_backtest import Simulator
import pandas as pd


def test_import_and_run():
    data = pd.DataFrame({
        "close": [100 + i for i in range(100)]
    })

    sim = Simulator(data)
    equity = sim.run()

    assert isinstance(equity, float)
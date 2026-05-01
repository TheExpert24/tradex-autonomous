import pandas as pd
from run_backtest import Simulator


def make_data():
    return pd.DataFrame({
        "close": [100 + i for i in range(200)]
    })


def test_sim_runs():
    data = make_data()
    sim = Simulator(data)

    final_equity = sim.run()

    assert final_equity > 0
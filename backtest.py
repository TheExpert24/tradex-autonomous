from market.market_data import MarketData
from market.orderbook import OrderBook
from broker.broker import Broker
from broker.execution_model import ExecutionModel
from strategy.mean_reversion import MeanReversionStrategy
from engine.sim_engine import SimEngine

def main():
    md = MarketData()
    ob = OrderBook()
    exec_model = ExecutionModel()

    broker = Broker(ob, exec_model)
    strat = MeanReversionStrategy()

    engine = SimEngine(md, broker, strat)
    engine.run(steps=2000)

if __name__ == "__main__":
    main()
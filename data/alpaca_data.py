import alpaca_trade_api as tradeapi
from config.config import API_KEY, SECRET_KEY, BASE_URL

class DataClient:
    def __init__(self):
        self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)

    def get_bars(self, symbol, limit=200):
        return self.api.get_bars(symbol, "1Min", limit=limit).df
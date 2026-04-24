import alpaca_trade_api as tradeapi
from config.config import *

class Universe:
    def __init__(self, api):
        self.api = api

    def get_all_symbols(self):
        assets = self.api.list_assets()

        symbols = [
            a.symbol
            for a in assets
            if (
                a.tradable
                and a.status == "active"
                and a.exchange in ["NASDAQ", "NYSE"]
                and "." not in a.symbol
                and "-" not in a.symbol
            )
        ]

        return symbols
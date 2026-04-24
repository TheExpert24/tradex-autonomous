import alpaca_trade_api as tradeapi
from config.config import API_KEY, SECRET_KEY, BASE_URL

class Executor:
    def __init__(self):
        self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)

    def account(self):
        return self.api.get_account()

    def buy(self, symbol, qty):
        return self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side="buy",
            type="market",
            time_in_force="day"
        )

    def sell(self, symbol, qty):
        return self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side="sell",
            type="market",
            time_in_force="day"
        )
from alpaca_trade_api.stream import Stream
from config.config import *

class StreamEngine:
    def __init__(self, symbols, callback):
        self.stream = Stream(API_KEY, SECRET_KEY, base_url=BASE_URL, data_feed="iex")
        self.symbols = symbols
        self.callback = callback

    def start(self):
        for s in self.symbols:
            self.stream.subscribe_bars(self._handler, s)

        self.stream.run()

    async def _handler(self, bar):
        self.callback(bar)
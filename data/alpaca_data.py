import pandas as pd
from datetime import datetime, timedelta

class DataClient:
    def __init__(self, api):
        self.api = api

    def get_bars(self, symbol):
        try:
            symbol = symbol.replace(".", "-")

            end = datetime.utcnow()
            start = end - timedelta(days=365)

            start_str = start.strftime("%Y-%m-%dT%H:%M:%SZ")
            end_str = end.strftime("%Y-%m-%dT%H:%M:%SZ")

            bars = self.api.get_bars(
                symbol,
                "1Day",
                start=start_str,
                end=end_str,
                feed="iex"
            ).df

            if bars is None or len(bars) == 0:
                return None

            if isinstance(bars.index, pd.MultiIndex):
                bars = bars.xs(symbol, level=1)

            required = ["open", "high", "low", "close", "volume"]

            for col in required:
                if col not in bars.columns:
                    return None

            bars = bars.dropna()

            return bars

        except Exception as e:
            print("DATA ERROR:", symbol, e)
            return None
class Universe:
    def __init__(self, api):
        self.api = api

    def get_all_symbols(self):
        try:
            assets = self.api.list_assets(status="active")

            symbols = []

            for a in assets:
                try:
                    if getattr(a, "tradable", False) and getattr(a, "symbol", None):
                        symbols.append(a.symbol)
                except:
                    continue

            return symbols

        except:
            return []
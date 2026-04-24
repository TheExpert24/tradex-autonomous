class PositionManager:
    def __init__(self, api):
        self.api = api

    def get_positions(self):
        return self.api.list_positions()

    def has_position(self, symbol):
        return symbol in [p.symbol for p in self.get_positions()]

    def get_position(self, symbol):
        positions = self.get_positions()
        for p in positions:
            if p.symbol == symbol:
                return p
        return None
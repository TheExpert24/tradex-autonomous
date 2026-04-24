class PositionManager:
    def __init__(self, api):
        self.api = api
        self.positions = {}

    def refresh(self):
        self.positions = {}
        for p in self.api.list_positions():
            self.positions[p.symbol] = p

    def has_position(self, symbol):
        return symbol in self.positions

    def position_count(self):
        return len(self.positions)

    def can_buy(self, symbol, max_positions):
        self.refresh()
        if self.has_position(symbol):
            return False
        if self.position_count() >= max_positions:
            return False
        return True
class Portfolio:
    def __init__(self, initial_cash=100000):
        self.cash = initial_cash
        self.positions = {}
        self.equity_curve = []

    def value(self, prices):
        total = self.cash
        for sym, pos in self.positions.items():
            if sym in prices:
                total += pos["qty"] * prices[sym]
        return total

    def buy(self, symbol, qty, price):
        cost = qty * price
        if self.cash < cost:
            return

        self.cash -= cost

        if symbol not in self.positions:
            self.positions[symbol] = {"qty": 0, "avg": 0}

        pos = self.positions[symbol]
        new_qty = pos["qty"] + qty
        pos["avg"] = (pos["qty"] * pos["avg"] + qty * price) / new_qty
        pos["qty"] = new_qty

    def sell(self, symbol, qty, price):
        if symbol not in self.positions:
            return

        pos = self.positions[symbol]
        qty = min(qty, pos["qty"])

        self.cash += qty * price
        pos["qty"] -= qty

        if pos["qty"] == 0:
            del self.positions[symbol]
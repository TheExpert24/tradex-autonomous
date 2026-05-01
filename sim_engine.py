import numpy as np

class SimEngine:
    def __init__(self, starting_capital=10000, fee=0.0003, slippage=0.0005):
        self.capital = starting_capital
        self.fee = fee
        self.slippage = slippage
        self.positions = {}
        self.entry_prices = {}
        self.equity_curve = []

    def _apply_slippage(self, price, side):
        if side == "buy":
            return price * (1 + self.slippage)
        else:
            return price * (1 - self.slippage)

    def mark_to_market(self, prices):
        total = self.capital

        for sym, qty in self.positions.items():
            if sym in prices:
                total += qty * prices[sym]

        self.equity_curve.append(total)
        return total

    def execute(self, symbol, action, price, signal_strength=1.0):
        price = float(price)

        if action == "HOLD":
            return

        # EXIT position
        if action == "EXIT" and symbol in self.positions:
            qty = self.positions[symbol]

            exec_price = self._apply_slippage(price, "sell" if qty > 0 else "buy")

            pnl = qty * (exec_price - self.entry_prices[symbol])
            cost = abs(qty * exec_price) * self.fee

            self.capital += pnl - cost

            del self.positions[symbol]
            del self.entry_prices[symbol]

            return

        # ENTER LONG
        if action == "ENTER_LONG":
            if symbol in self.positions:
                return

            alloc = self.capital * 0.05
            qty = alloc / price

            exec_price = self._apply_slippage(price, "buy")

            self.positions[symbol] = qty
            self.entry_prices[symbol] = exec_price

            cost = alloc * self.fee
            self.capital -= cost

        # ENTER SHORT
        if action == "ENTER_SHORT":
            if symbol in self.positions:
                return

            alloc = self.capital * 0.05
            qty = -alloc / price

            exec_price = self._apply_slippage(price, "sell")

            self.positions[symbol] = qty
            self.entry_prices[symbol] = exec_price

            cost = alloc * self.fee
            self.capital -= cost

    def get_equity(self, prices):
        mtm = self.mark_to_market(prices)
        return mtm

    def summary(self):
        return {
            "capital": self.capital,
            "positions": len(self.positions),
            "equity_curve": self.equity_curve[-1] if self.equity_curve else self.capital
        }
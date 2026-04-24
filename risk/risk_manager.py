class RiskManager:
    def __init__(self, max_risk_per_trade=0.01, max_positions=10, max_drawdown=0.1):
        self.max_risk_per_trade = max_risk_per_trade
        self.max_positions = max_positions
        self.max_drawdown = max_drawdown

    def position_size(self, equity, price):
        risk_dollars = equity * self.max_risk_per_trade
        qty = int(risk_dollars / price)
        return max(qty, 0)

    def check_drawdown(self, start_equity, current_equity):
        dd = (start_equity - current_equity) / start_equity
        return dd > self.max_drawdown

    def can_open_new_position(self, current_positions):
        return len(current_positions) < self.max_positions
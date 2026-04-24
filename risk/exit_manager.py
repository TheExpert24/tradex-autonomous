class ExitManager:
    def __init__(self, api):
        self.api = api

    def should_exit(self, position, current_price):
        entry_price = float(position.avg_entry_price)

        pnl_pct = (current_price - entry_price) / entry_price

        if pnl_pct <= -0.03:
            return True

        if pnl_pct >= 0.05:
            return True

        return False
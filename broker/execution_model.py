import random

class ExecutionModel:
    def __init__(self, latency=1, fee_bps=1):
        self.latency = latency
        self.fee_bps = fee_bps

    def fill_price(self, side, price, spread):
        slippage = random.uniform(0, spread * 0.3)

        if side == "buy":
            return price + slippage
        else:
            return price - slippage

    def apply_fees(self, price, qty):
        return price * qty * (self.fee_bps / 10000)
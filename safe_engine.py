import numpy as np

class SafeEngine:
    def __init__(self, threshold=0.1):
        self.threshold = threshold
        self.positions = {}

    def signal_to_action(self, symbol, signal):
        position = self.positions.get(symbol)

        # no position → maybe enter
        if position is None:
            if signal > self.threshold:
                return "ENTER_LONG"
            elif signal < -self.threshold:
                return "ENTER_SHORT"
            return "HOLD"

        # already long
        if position == "long":
            if signal < 0:
                return "EXIT"
            return "HOLD"

        # already short
        if position == "short":
            if signal > 0:
                return "EXIT"
            return "HOLD"

    def update_position(self, symbol, action):
        if action == "ENTER_LONG":
            self.positions[symbol] = "long"
        elif action == "ENTER_SHORT":
            self.positions[symbol] = "short"
        elif action == "EXIT":
            self.positions.pop(symbol, None)
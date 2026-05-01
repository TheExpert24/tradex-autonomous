from collections import deque

class Broker:
    def __init__(self, orderbook, exec_model):
        self.ob = orderbook
        self.exec = exec_model
        self.pending = deque()
        self.cash = 100000
        self.position = 0

    def send_order(self, order):
        self.pending.append(order)

    def step(self):
        fills = []

        for _ in range(len(self.pending)):
            order = self.pending.popleft()
            result = self.ob.match(order)

            for price, qty in result:
                if order.side == "buy":
                    self.position += qty
                    self.cash -= price * qty
                else:
                    self.position -= qty
                    self.cash += price * qty

                fills.append((price, qty))

        return fills

    def equity(self, mid):
        return self.cash + self.position * mid
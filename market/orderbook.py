from collections import deque
import bisect
import random

class Order:
    def __init__(self, price, qty, side, order_id, ts):
        self.price = price
        self.qty = qty
        self.side = side  # "buy" / "sell"
        self.id = order_id
        self.ts = ts


class OrderBook:
    def __init__(self):
        self.bids = []  # sorted desc
        self.asks = []  # sorted asc
        self.bid_map = {}
        self.ask_map = {}

    def mid(self):
        if not self.bids or not self.asks:
            return None
        return (self.bids[0][0] + self.asks[0][0]) / 2

    def spread(self):
        if not self.bids or not self.asks:
            return None
        return self.asks[0][0] - self.bids[0][0]

    def add_limit(self, order: Order):
        book = self.bids if order.side == "buy" else self.asks
        key = -order.price if order.side == "buy" else order.price

        bisect.insort(book, (order.price, order))

    def match(self, order: Order):
        """Immediate-or-cancel marketable order"""
        fills = []

        if order.side == "buy":
            while self.asks and order.qty > 0:
                best_price, best = self.asks[0]
                if order.price < best_price:
                    break

                qty = min(order.qty, best.qty)
                order.qty -= qty
                best.qty -= qty
                fills.append((best_price, qty))

                if best.qty == 0:
                    self.asks.pop(0)

        else:
            while self.bids and order.qty > 0:
                best_price, best = self.bids[0]
                if order.price > best_price:
                    break

                qty = min(order.qty, best.qty)
                order.qty -= qty
                best.qty -= qty
                fills.append((best_price, qty))

                if best.qty == 0:
                    self.bids.pop(0)

        return fills
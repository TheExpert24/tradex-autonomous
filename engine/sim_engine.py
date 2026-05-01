class SimEngine:
    def __init__(self, md, broker, strategy):
        self.md = md
        self.broker = broker
        self.strategy = strategy

    def run(self, steps=10000):
        for i in range(steps):
            data = self.md.tick()

            self.strategy.on_tick(data, self.broker)

            self.broker.step()

            if i % 50 == 0:
                eq = self.broker.equity(data["mid"])
                print(f"step {i} equity: {eq:.2f}")
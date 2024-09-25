import mt5_api as mt5


class Bot:
    def __init__(self, bot_id, strategy):
        self.bot_id: int = bot_id
        self.strategy = strategy
        self.positions = []

    def trade(self):
        signal = self.check_signal()
        position = self.send_order(signal)

        if position:
            self.positions.append(position)

    def stop_trade(self):
        for position in self.positions:
            mt5.close_position(position)
            self.positions.remove(position)

    def check_signal(self):
        return self.strategy.check_signal()

    def send_order(self, signal):
        return self.strategy.send_order(signal)

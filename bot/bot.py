from datetime import datetime

import mt5_api as mt5


class Bot:
    def __init__(self, bot_id, strategy):
        self.bot_id: int = bot_id
        self.strategy = strategy
        self.positions = []
    #
    # def __getattribute__(self, name):
    #     self.update_position()
    #
    #     return super().__getattribute__(name)

    def update_position(self):
        for i in range(len(self.positions)):
            self.positions[i] = mt5.positions_get(ticket=self.positions[i].ticket)

    def trade(self):
        print(f"Bot: I am trading with {self.strategy}:{datetime.now()}")
        signal = self.check_signal()
        print(f"check for signal: {signal}")
        position = self.send_order(signal)

        if position:
            print(f"opened position: {position}")
            self.positions.append(position)

    def stop_trade(self):
        for position in self.positions:
            mt5.close_position(position)
            self.positions.remove(position)

    def check_signal(self):
        return self.strategy.check_signal(self.positions)

    def send_order(self, signal):
        return self.strategy.send_order(signal, self.positions)

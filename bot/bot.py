import mt5_api as mt5


class Bot:
    def __init__(self, bot_id):
        self.bot_id: int = bot_id
        self.positions = []
        self.strategy

    def trade(self):
        self.check_signal()
        self.trade()

    def stop_trade(self):
        for position in self.positions:
            mt5.close_position(position)

    def check_signal(self):
        pass

    def send_order(self):
        pass

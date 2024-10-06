class BotTrade:
    def __init__(self, bot_id, strategy):
        self.bot_id: int = bot_id
        self.strategy = strategy

    def trade(self):
        self.check_signal()
        self.send_order()
        self.report()

    def check_signal(self):
        self.strategy.check_signal()

    def send_order(self):
        self.strategy.send_order()

    def report(self):
        self.strategy.report()

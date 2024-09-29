from datetime import datetime

import mt5_api as mt5


class BotTrade:
    def __init__(self, bot_id, strategy):
        self.bot_id: int = bot_id
        self.strategy = strategy

    def trade(self):
        print("begin trade")
        self.check_signal()
        self.send_order()
        self.report()
        print("end trade")

    def check_signal(self):
        print("begin check signal")
        self.strategy.check_signal()
        print("end check signal")

    def send_order(self):
        print("begin send order")
        self.strategy.send_order()
        print("end send order")

    def report(self):
        print("begin report")
        self.strategy.report()
        print("end report")

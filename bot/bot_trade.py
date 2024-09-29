from datetime import datetime

import mt5_api as mt5


class BotTrade:
    def __init__(self, bot_id, strategy):
        self.bot_id: int = bot_id
        self.strategy = strategy
        self.order_tickets = []

    def trade(self):
        print(f"[{datetime.now()}] :: Bot: I am trading using {type(self.strategy).__name__}")
        signal = self.check_signal()
        print(f"[{datetime.now()}] :: Strategy: {type(self.strategy).__name__}: check for signal: {signal}")
        order_ticket = self.send_order(signal)

        if order_ticket:
            print(f"[{datetime.now()}] :: Strategy: {type(self.strategy).__name__} opened order: {order_ticket}")
            self.order_tickets.append(order_ticket)

    def stop_trade(self):
        for order_ticket in self.order_tickets:
            mt5.close_position(order_ticket)
            self.order_tickets.remove(order_ticket)

    def check_signal(self):
        return self.strategy.check_signal(self.order_tickets)

    def send_order(self, signal):
        return self.strategy.send_order(signal, self.order_tickets)

import script.mt5.mt5_api as mt5


class BotTrade:
    def __init__(self, bot_id):
        self.bot_id: int = bot_id
        self.position_ticket = None

    def trade(self, signal):
        self.position_ticket = mt5.place_trade("BTCUSD", 0.01, signal)

    def update(self, signal):
        self.trade(signal)

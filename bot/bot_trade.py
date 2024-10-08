class BotTrade:
    def __init__(self, bot_id):
        self.bot_id: int = bot_id
        self.position_ticket = None

    def trade(self, signal):
        print(f"Bot: {self.bot_id} Trade: {signal}")

    def update(self, signal):
        self.trade(signal)

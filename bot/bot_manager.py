from bot.bot_trade import BotTrade


class BotManager:
    def __init__(self, bots: list[BotTrade] = None):
        if bots is None:
            self.bots = []
        else:
            self.bots = bots

    def create_new_bot(self, strategy):
        bot_id = 1
        while True:
            if bot_id not in [bot.bot_id for bot in self.bots]:
                break
            bot_id += 1

        bot = BotTrade(bot_id, strategy)
        self.bots.append(bot)

        return bot

    def get_bot(self, bot_id):
        for bot in self.bots:
            if bot.bot_id == bot_id:
                return bot
        raise ValueError(f'Bot with bot_id {bot_id} not found')

    def stop(self):
        for bot in self.bots:
            bot.stop_trade()
            self.bots.remove(bot)

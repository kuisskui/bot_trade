from bot.bot_trade import BotTrade


class BotManager:
    def __init__(self, bots: list[BotTrade] = None):
        if bots is None:
            self.__bots = []
        else:
            self.__bots = bots

    def create_new_bot(self, strategy):
        bot_id = 1
        while True:
            if bot_id not in [bot.bot_id for bot in self.__bots]:
                break
            bot_id += 1

        bot = BotTrade(bot_id, strategy)
        self.__bots.append(bot)

        return bot

    def get_bots(self):
        return self.__bots


bot_manager = BotManager()

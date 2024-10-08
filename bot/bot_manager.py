from bot.bot_trade import BotTrade
from typing import List


class BotManager:
    def __init__(self):
        self.__bots: List[BotTrade] = []

    def create_new_bot(self):
        bot_id = 1
        while True:
            if bot_id not in [bot.bot_id for bot in self.__bots]:
                break
            bot_id += 1

        bot = BotTrade(bot_id)
        self.__bots.append(bot)

        return bot

    def get_bots(self):
        return self.__bots


bot_manager = BotManager()

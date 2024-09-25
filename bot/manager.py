from .bot import Bot


class BotManager:
    def __init__(self, bots: list[Bot] = None):
        if bots is None:
            self.bots = []
        self.bots = bots

    def create_new_bot(self, bot_id=None):
        if bot_id is None:
            gen_id = len(self.bots)
            self.create_new_bot(gen_id)

        if bot_id in [bot.bot_id for bot in self.bots]:
            bot_id += 1
            self.create_new_bot(bot_id)

        bot = Bot(bot_id)
        self.bots.append(bot)

        return bot

    def get_bot(self, bot_id):
        for bot in self.bots:
            if bot.bot_id == bot_id:
                return bot
        raise ValueError(f'Bot with bot_id {bot_id} not found')

    def stop(self):
        for bot in self.bots:
            bot.stop()
            self.bots.remove(bot)

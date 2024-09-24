from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Bot:
    def __init__(self, strategy):
        self.strategy = strategy
        self.positions = []

    def start(self):
        print('Bot: start is called')
        self.strategy.start()

    def check(self) -> int:
        pass

    def trade(self):
        pass

    def stop(self):
        print('Bot: stop is called')
        self.strategy.stop()


class Bot:
    def __init__(self, strategy):
        self.strategy = strategy

    def start(self):
        print('Bot: start is called')
        self.strategy.start()

    def stop(self):
        print('Bot: stop is called')


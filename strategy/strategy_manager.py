from strategy import Strategy
from typing import List


class StrategyManager:
    def __init__(self):
        self.strategies: List[Strategy] = []

    def add_strategy(self, strategy: Strategy):
        self.strategies.append(strategy)
        return strategy

    def remove_strategy(self, strategy: Strategy):
        self.strategies.remove(strategy)


strategy_manager = StrategyManager()

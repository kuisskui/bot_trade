from .strategy import Strategy
from typing import List


class StrategyManager:
    def __init__(self):
        self.__strategies: List[Strategy] = []

    def add_strategy(self, strategy: Strategy):
        self.__strategies.append(strategy)
        return strategy

    def remove_strategy(self, strategy: Strategy):
        self.__strategies.remove(strategy)

    def get_strategies(self):
        return self.__strategies


strategy_manager = StrategyManager()

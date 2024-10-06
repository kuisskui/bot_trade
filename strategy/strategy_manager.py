import os

from strategy.strategy import Strategy
from typing import List


class StrategyManager:
    def __init__(self):
        self.__active_strategies: List[Strategy] = []

    def add_strategy(self, strategy: Strategy):
        self.__active_strategies.append(strategy)
        return strategy

    def remove_strategy(self, strategy: Strategy):
        self.__active_strategies.remove(strategy)

    def get_all_strategies(self):
        return

    def get_active_strategies(self):
        return self.__active_strategies


strategy_manager = StrategyManager()

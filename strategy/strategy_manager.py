from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from strategy.strategy import Strategy
from typing import List
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
BASE_DIR = Path(os.getenv("BASE_DIR"))
SCRIPT_DIR = BASE_DIR / os.getenv("SCRIPT_DIR")

scheduler = AsyncIOScheduler()


class StrategyManager:
    def __init__(self):
        self.__active_strategies: List[Strategy] = []

    def add_strategy(self, strategy: Strategy):
        self.__active_strategies.append(strategy)
        return strategy

    def run_new_strategy(self, state):
        strategy_id = 1
        while True:
            if strategy_id not in [strategy.strategy_id for strategy in self.__active_strategies]:
                break
            strategy_id += 1

        strategy = Strategy(strategy_id, state)
        strategy.run()

        self.add_strategy(strategy)
        return strategy

    def remove_strategy(self, strategy: Strategy):
        self.__active_strategies.remove(strategy)
        scheduler.remove_job(str(strategy.strategy_id))

    def get_all_strategies(self):
        return [f for f in os.listdir(SCRIPT_DIR) if f.endswith('.py')]

    def get_active_strategies(self):
        return self.__active_strategies

    def get_strategy_by_id(self, strategy_id):
        for strategy in self.__active_strategies:
            if strategy.strategy_id == strategy_id:
                return strategy


strategy_manager = StrategyManager()

from copy import deepcopy
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import os
import subprocess
import json
import sys

from strategy.order import Order
from bot.bot_trade import BotTrade
load_dotenv()

BASE_DIR = Path(os.getenv("BASE_DIR"))
SCRIPT_DIR = BASE_DIR / os.getenv("SCRIPT_DIR")

scheduler = AsyncIOScheduler()
scheduler.start()


class Strategy:
    def __init__(self, strategy_id, state):
        self.strategy_id: int = strategy_id
        self.subscribers: List[BotTrade] = []

        self.state = state

        self.script = deepcopy(state['script'])
        self.trigger = deepcopy(state['trigger'])

    def run(self):
        scheduler.add_job(
            self.get_signal,
            trigger=CronTrigger(**self.trigger),
            id=str(self.strategy_id)
        )

    def get_signal(self):
        # Life cycle of Strategy
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / self.script), json.dumps(self.state)],
                capture_output=True,
                text=True
            )

            json_data = json.loads(result.stdout.strip())

            orders = self.parse_order(json_data)

            for order in orders:
                self.notify_subscribers(order)

        except subprocess.CalledProcessError as e:
            print("Error: ", e.stderr)

    def parse_order(self, json_data) -> List[Order]:
        orders: List[Order] = []
        if isinstance(json_data, list):
            for order_dict in json_data:
                order = Order(order_dict['symbol'], order_dict['order_type'])
                orders.append(order)

        if isinstance(json_data, dict):
            order_dict: dict = json_data
            order = Order(order_dict['symbol'], order_dict['order_type'])
            orders.append(order)

        return orders

    def subscribe(self, subscriber: BotTrade):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: BotTrade):
        self.subscribers.remove(subscriber)

    def notify_subscribers(self, order: Order):
        for subscriber in self.subscribers:
            subscriber.update(order)

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


def parse_order(order) -> List[Order]:
    orders: List[Order] = []
    if isinstance(order, list):
        for order_dict in order:
            order = Order(order_dict['symbol'], order_dict['order_type'])
            orders.append(order)

    if isinstance(order, dict):
        order_dict: dict = order
        order = Order(order_dict['symbol'], order_dict['order_type'])
        orders.append(order)

    return orders


class Strategy:
    def __init__(self, strategy_id, state):
        self.strategy_id: int = strategy_id
        self.subscribers: List[BotTrade] = []
        self.state = state
        self.job = None

    def run(self):
        self.start()

    def get_signal(self):
        self.pre_execute()

        self.execute()

        self.post_execute()

    def start(self):
        self.job = scheduler.add_job(
            self.get_signal,
            trigger=CronTrigger(**self.state['trigger']),
            id=str(self.strategy_id)
        )

    def exit(self):
        self.job.remove()

    def pre_execute(self):
        pass

    def execute(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / self.state['script']), json.dumps(self.state)],
            capture_output=True,
            text=True
        )
        self.state = json.loads(result.stdout.strip())

    def post_execute(self):
        self.job.modify(trigger=CronTrigger(**self.state['trigger']))
        self.notify_subscribers()

    def notify_subscribers(self):
        if not self.state.get('order'):
            return

        orders = parse_order(self.state['order'])

        for subscriber in self.subscribers:
            for order in orders:
                subscriber.update(order)

    def subscribe(self, subscriber: BotTrade):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: BotTrade):
        self.subscribers.remove(subscriber)

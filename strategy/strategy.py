from pathlib import Path
from typing import List
from dotenv import load_dotenv
import os
import subprocess
import json
import sys

from order import Order
from bot.bot_trade import BotTrade
load_dotenv()

BASE_DIR = Path(os.getenv("BASE_DIR"))
SCRIPT_DIR = BASE_DIR / os.getenv("SCRIPT_DIR")


class Strategy:
    def __init__(self, strategy_id, script, state):
        self.strategy_id: int = strategy_id
        self.script = script
        self.state = state
        self.subscribers: List[BotTrade] = []

    def get_signal(self):
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / self.script), json.dumps(self.state)],
                capture_output=True,
                text=True
            )

            json_data = json.loads(result.stdout.strip())

            if isinstance(json_data, list):
                for order_dict in json_data:
                    order = Order(order_dict.get('symbol'), order_dict.get('order_type'))
                    self.notify_subscribers(order)
            if isinstance(json_data, dict):
                order_dict: dict = json_data
                order = Order(order_dict.get('symbol'), order_dict.get('order_type'))
                self.notify_subscribers(order)

        except subprocess.CalledProcessError as e:
            print("Error: ", e.stderr)

    def subscribe(self, subscriber: BotTrade):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: BotTrade):
        self.subscribers.remove(subscriber)

    def notify_subscribers(self, order: Order):
        for subscriber in self.subscribers:
            subscriber.update(order)

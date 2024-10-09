from pathlib import Path
from typing import List
from dotenv import load_dotenv
import os
import subprocess
import json
import sys

from bot.bot_trade import BotTrade
load_dotenv()

BASE_DIR = Path(os.getenv("BASE_DIR"))
SCRIPT_DIR = BASE_DIR / os.getenv("SCRIPT_DIR")


class Strategy:
    def __init__(self, strategy_id, script, state):
        self.strategy_id: int = strategy_id
        self.script = script
        self.state = state
        self.signal = None
        self.subscribers: List[BotTrade] = []

    def get_signal(self):
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / self.script), json.dumps(self.state)],
                capture_output=True,
                text=True
            )
            output = result.stdout.strip()
            self.state = json.loads(output)
            self.signal = self.state.get("signal")

        except subprocess.CalledProcessError as e:
            print("Error: ", e.stderr)
            self.signal = None
        finally:
            self.notify_subscribers()

    def subscribe(self, subscriber: BotTrade):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: BotTrade):
        self.subscribers.remove(subscriber)

    def notify_subscribers(self):
        for subscriber in self.subscribers:
            subscriber.update(self.signal)

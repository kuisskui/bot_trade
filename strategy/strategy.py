from pathlib import Path
from dotenv import load_dotenv
import os
import subprocess
import json
import sys

load_dotenv()

BASE_DIR = Path(os.getenv("BASE_DIR"))
SCRIPT_DIR = BASE_DIR / os.getenv("SCRIPT_DIR")


class Strategy:
    def __init__(self, strategy_id, script, state):
        self.strategy_id = strategy_id
        self.script = script
        self.state = state
        self.signal = None

    def get_signal(self):
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / self.script), json.dumps(self.state)],
                capture_output=True,
                text=True
            )
            self.signal = result.stdout.strip()

        except subprocess.CalledProcessError as e:
            print("Error: ", e.stderr)
            return None

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
    def __init__(self, script, state):
        self.script = script
        self.state = state

    def get_signal(self):
        try:
            print(str(SCRIPT_DIR / self.script))
            result = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / self.script), self.state],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()

        except subprocess.CalledProcessError as e:
            print("Error: ", e.stderr)
            return None

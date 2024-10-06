import json
import os
import subprocess
import sys


class Strategy:
    def __init__(self, script, **kwargs):
        self.script = os.path.join(os.path.dirname(__file__), "script", script)
        self.kwargs = kwargs

    def get_signal(self):
        try:
            json_str = json.dumps(self.kwargs)

            result = subprocess.run(
                [sys.executable, self.script, json_str],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()

        except subprocess.CalledProcessError as e:
            print("Error: ", e.stderr)
            return None

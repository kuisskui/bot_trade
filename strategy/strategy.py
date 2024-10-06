import subprocess
import os


class Strategy:
    def __init__(self, script):
        self.script = os.path.join(os.path.dirname(__file__), script)

    def get_signal(self, json):
        try:
            result = subprocess.run(
                ["python", self.script, json],
                capture_output=True,
                text=True
            )
            print(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print("Error: ", e.stderr)

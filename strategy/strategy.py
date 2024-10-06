import json
import os
import subprocess
import sys


class Strategy:
    def __init__(self, script):
        self.script = os.path.join(os.path.dirname(__file__), "script", script)

    def get_signal(self, json_data={"symbol": "BTCUSD"}):
        try:
            # Convert the dictionary to a properly formatted JSON string
            json_str = json.dumps(json_data)

            result = subprocess.run(
                [sys.executable, self.script, json_str],  # Pass the JSON string to the script
                capture_output=True,
                text=True
            )

            # Print the Python executable path for confirmation
            print(sys.executable)

            # Output result from the subprocess
            print("Output:", result.stdout.strip())
            return result.stdout

        except subprocess.CalledProcessError as e:
            print("Error: ", e.stderr)
            return None

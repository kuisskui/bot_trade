import json
import sys
import random

input_data: dict = json.loads(sys.argv[1])

num = random.randint(1, 100)
signal = "buy" if num % 2 == 0 else "sell"

output_data = input_data | {"signal": signal}

print(json.dumps(output_data))

import random
import json
import sys

json = json.loads(sys.argv[1])
num = random.randint(1, 100)
x = "buy" if num % 2 == 0 else "sell"
print(x)

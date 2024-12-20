import json
import sys
import random
from strategy.order import Order
from api.api import end
input_data: dict = json.loads(sys.argv[1])

num = random.randint(1, 100)
signal = "buy" if num % 2 == 0 else "sell"

output_data = input_data | {"order" : Order("BTCUSD", signal).__dict__}

end(output_data)

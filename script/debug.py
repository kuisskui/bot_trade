import random
from strategy.order import Order
from api.api import *

state: dict = get_state()
symbol = state["symbol"]

num = random.randint(1, 100)
signal = "buy" if num % 2 == 0 else "sell"

new_order = Order(symbol, signal)
new_state = {"order": new_order.__dict__}
    
state = update_state(state, new_state)

end(state)

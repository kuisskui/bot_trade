from strategy.order import Order
from api import mt5_api
from indicator.indicator import get_relative_strength_index
from api.api import *

current_state = get_state()

symbol = current_state['symbol']
time_frame = current_state['time_frame']

overbought = 70
oversold = 30
period = 14

mt5_api.initialize()
previous_rsi = get_relative_strength_index(symbol, time_frame, 2, period)
current_rsi = get_relative_strength_index(symbol, time_frame, 1, period)

if previous_rsi > overbought > current_rsi:
    order = Order(symbol, "sell")
elif previous_rsi < oversold < current_rsi:
    order = Order(symbol, "buy")
else:
    order = Order(symbol, "hold")
new_state = {"order": order}
current_state = update_state(current_state, new_state)

end(current_state)

import json
import sys
from strategy.order import Order
from mt5 import mt5_api
from indicator.indicator import get_relative_strength_index


class RSIStrategy:
    def __init__(self, symbol, time_frame):
        self.symbol = symbol
        self.time_frame = time_frame

        self.overbought = 70
        self.oversold = 30
        self.period = 14

    def get_signal(self):
        mt5_api.initialize()
        previous_rsi = get_relative_strength_index(self.symbol, self.time_frame, 1, self.period)
        current_rsi = get_relative_strength_index(self.symbol, self.time_frame, 0, self.period)

        if previous_rsi > self.overbought > current_rsi:
            return 'sell'
        elif previous_rsi < self.oversold < current_rsi:
            return 'buy'
        return 'hold'


if __name__ == "__main__":
    json_data = json.loads(sys.argv[1])
    symbol = json_data['symbol']
    time_frame = json_data['time_frame']
    strategy = RSIStrategy(symbol, time_frame)
    order = Order(json_data['symbol'], strategy.get_signal())
    print(json.dumps(order))

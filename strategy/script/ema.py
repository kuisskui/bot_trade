import mt5_api
from datetime import datetime
from strategy.script.indicator import get_exponential_moving_average


class ExponentialMovingAverageCrossingOverStrategy:
    def __init__(self, symbol, time_frame=mt5_api.TIMEFRAME_M1, lot=0.1, short_period=5, long_period=20):
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.short_period = short_period
        self.long_period = long_period
        self.previous_short_ma = None
        self.previous_long_ma = None

    def check_signal(self, positions):
        mt5_api.initialize()
        current_short_ma = get_exponential_moving_average(symbol=self.symbol, timeframe=self.time_frame, shift=0, period=self.short_period)
        current_long_ma = get_exponential_moving_average(symbol=self.symbol, timeframe=self.time_frame, shift=0,  period=self.long_period)

        if self.previous_short_ma is None or self.previous_long_ma is None:
            self.previous_short_ma = current_short_ma
            self.previous_long_ma = current_long_ma
            return "hold"

        crossed_up = self.previous_short_ma <= self.previous_long_ma and current_short_ma > current_long_ma
        crossed_down = self.previous_short_ma >= self.previous_long_ma and current_short_ma < current_long_ma

        print(f"[{datetime.now()}] :: {type(self).__name__} : EMA crossing check: crossed_up={crossed_up}, crossed_down={crossed_down}")

        if crossed_up:
            signal = "buy"
        elif crossed_down:
            signal = "sell"
        else:
            signal = "hold"

        self.previous_short_ma = current_short_ma
        self.previous_long_ma = current_long_ma

        return signal

    def send_order(self, signal, positions):
        position = None
        active_positions = mt5_api.positions_get(symbol=self.symbol)
        if signal == "buy":
            if not active_positions:
                position = mt5_api.place_trade(self.symbol, self.lot, "buy")

            elif active_positions[0].type == 1:
                mt5_api.close_position(active_positions[0])
                position = mt5_api.place_trade(self.symbol, self.lot, "buy")

        elif signal == "sell":
            if not active_positions:
                position = mt5_api.place_trade(self.symbol, self.lot, "sell")
            elif active_positions[0].type == 0:
                mt5_api.close_position(active_positions[0])
                position = mt5_api.place_trade(self.symbol, self.lot, "sell")
        return position

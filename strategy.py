import mt5_api
from indicator import get_moving_average, get_relative_strength_index


class MovingAverageCrossingOverStrategy:
    def __init__(self, symbol, time_frame, lot, short_period, long_period):
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.short_period = short_period
        self.long_period = long_period
        self.previous_short_ma = None
        self.previous_long_ma = None

    def check_signal(self):
        mt5_api.initialize()
        current_short_ma = get_moving_average(self.symbol, self.time_frame, self.short_period)
        current_long_ma = get_moving_average(self.symbol, self.time_frame, self.long_period)

        # If this is the first run, store the MAs and return (no crossover check yet)
        if self.previous_short_ma is None or self.previous_long_ma is None:
            self.previous_short_ma = current_short_ma
            self.previous_long_ma = current_long_ma
            print("KuiBot: set ma")
            return True

        crossed_up = self.previous_short_ma <= self.previous_long_ma and current_short_ma > current_long_ma
        crossed_down = self.previous_short_ma >= self.previous_long_ma and current_short_ma < current_long_ma

        # print(f"MA crossing check: crossed_up={crossed_up}, crossed_down={crossed_down}")

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
        global position
        if signal == "buy":
            active_positions = mt5_api.positions_get(symbol=self.symbol)
            if not active_positions:
                position = mt5_api.place_trade(self.symbol, self.lot, "buy")

            elif active_positions[0].type == 1:
                current_position = mt5_api.positions_get(symbol=self.symbol)
                mt5_api.close_position(current_position)
                position = mt5_api.place_trade(self.symbol, self.lot, "buy")

        elif signal == "sell":
            active_positions = mt5_api.positions_get(symbol=self.symbol)
            if not active_positions:
                position = mt5_api.place_trade(self.symbol, self.lot, "sell")
            elif active_positions[0].type == 0:
                current_position = mt5_api.positions_get(symbol=self.symbol)
                mt5_api.close_position(current_position)
                position = mt5_api.place_trade(self.symbol, self.lot, "sell")
        return position


class RSIStrategy:
    def __init__(self, symbol, time_frame, lot, overbought, oversold):
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.overbought = overbought
        self.oversold = oversold

    def check_signal(self):
        mt5_api.initialize()
        rsi = get_relative_strength_index(self.symbol, self.time_frame)
        if rsi > self.overbought:
            signal = "sell"
        elif rsi < self.oversold:
            signal = "buy"
        else:
            signal = "hold"
        return signal

    def send_order(self, signal, positions):
        global position
        if signal == "buy":
            active_positions = mt5_api.positions_get(symbol=self.symbol)
            if not active_positions:
                position = mt5_api.place_trade(self.symbol, self.lot, "buy")

            elif active_positions[0].type == 1:
                current_position = mt5_api.positions_get(symbol=self.symbol)
                mt5_api.close_position(current_position)
                position = mt5_api.place_trade(self.symbol, self.lot, "buy")

        elif signal == "sell":
            active_positions = mt5_api.positions_get(symbol=self.symbol)
            if not active_positions:
                position = mt5_api.place_trade(self.symbol, self.lot, "sell")
            elif active_positions[0].type == 0:
                current_position = mt5_api.positions_get(symbol=self.symbol)
                mt5_api.close_position(current_position)
                position = mt5_api.place_trade(self.symbol, self.lot, "sell")
        return position

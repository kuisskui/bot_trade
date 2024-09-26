import mt5_api
from datetime import datetime
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

    def check_signal(self, positions):
        mt5_api.initialize()
        current_short_ma = get_moving_average(self.symbol, self.time_frame, self.short_period)
        current_long_ma = get_moving_average(self.symbol, self.time_frame, self.long_period)

        # If this is the first run, store the MAs and return (no crossover check yet)
        if self.previous_short_ma is None or self.previous_long_ma is None:
            self.previous_short_ma = current_short_ma
            self.previous_long_ma = current_long_ma
            return "hold"

        crossed_up = self.previous_short_ma <= self.previous_long_ma and current_short_ma > current_long_ma
        crossed_down = self.previous_short_ma >= self.previous_long_ma and current_short_ma < current_long_ma

        print(f"[{datetime.now()}] :: {type(self).__name__} : MA crossing check: crossed_up={crossed_up}, crossed_down={crossed_down}")

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


class RSIStrategy:
    def __init__(self, symbol, time_frame, lot, overbought, oversold):
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.overbought = overbought
        self.oversold = oversold

    def check_signal(self, positions):
        # this strategy might check and return hold until the port is broken if the market is dum to a way
        global signal
        mt5_api.initialize()
        rsi = get_relative_strength_index(self.symbol, self.time_frame)
        print(f"[{datetime.now()}] :: {type(self).__name__} : RSI for now: {rsi}")
        active_positions = mt5_api.positions_get(symbol=self.symbol)
        if active_positions:
            if active_positions[0].type == 1:
                if rsi <= 50:
                    signal = "exit"
                else:
                    signal = "hold"
            elif active_positions[0].type == 0:
                if rsi >= 50:
                    signal = "exit"
                else:
                    signal = "hold"
            else:
                signal = "hold"
            return signal

        if rsi > self.overbought:
            signal = "sell"
        elif rsi < self.oversold:
            signal = "buy"
        else:
            signal = "hold"
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

        elif signal == "exit":
            if active_positions:
                mt5_api.close_position(active_positions[0])
        return position


class NoAnalyzeStrategy:
    def __init__(self, symbol, time_frame, lot, point):
        pass

    def check_signal(self, positions):
        pass

    def send_order(self, signal, positions):
        pass

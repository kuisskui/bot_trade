import mt5_api
from datetime import datetime
from indicator import get_relative_strength_index


class RSIStrategy:
    def __init__(self, symbol, time_frame=mt5_api.TIMEFRAME_M1, lot=0.01, overbought=70, oversold=30):
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.overbought = overbought
        self.oversold = oversold

    def check_signal(self, positions):
        # this strategy might check and return hold until the port is broken if the market is dum to a way
        global signal
        mt5_api.initialize()
        rsi = get_relative_strength_index(self.symbol, self.time_frame, 0, 14)
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

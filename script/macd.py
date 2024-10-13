from script.api import mt5_api
from script.indicator.indicator import get_moving_average_convergence_divergence


class MACDStrategy:
    def __init__(self, symbol, time_frame, lot, short_period=12, long_period=26, signal_period=9):
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period

    def check_signal(self, positions):
        mt5_api.initialize()
        macd_line, signal_line = get_moving_average_convergence_divergence(self.symbol, self.time_frame,0, self.short_period, self.long_period, self.signal_period)

        if macd_line > signal_line:
            return "buy"
        elif macd_line < signal_line:
            return "sell"
        return "hold"

    def send_order(self, signal, positions):
        active_positions = mt5_api.positions_get(symbol=self.symbol)
        if signal == "buy" and (not active_positions or active_positions[0].type != 1):
            mt5_api.close_all_orders(self.symbol)
            return mt5_api.place_trade(self.symbol, self.lot, "buy")

        elif signal == "sell" and (not active_positions or active_positions[0].type != 0):
            mt5_api.close_all_orders(self.symbol)
            return mt5_api.place_trade(self.symbol, self.lot, "sell")
        return None

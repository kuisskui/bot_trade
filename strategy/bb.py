import mt5_api


class BollingerBandsStrategy:
    def __init__(self, symbol, time_frame, lot, period=20, std_dev=2):
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.period = period
        self.std_dev = std_dev

    def check_signal(self, positions):
        mt5_api.initialize()
        upper_band, lower_band, middle_band = get_bollinger_bands(self.symbol, self.time_frame, self.period, self.std_dev)
        current_price = mt5_api.get_current_price(self.symbol)

        if current_price < lower_band:
            return "buy"
        elif current_price > upper_band:
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

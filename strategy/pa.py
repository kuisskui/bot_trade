import mt5_api


class PriceActionStrategy:
    def __init__(self, symbol, time_frame, lot, support_level, resistance_level):
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.support_level = support_level
        self.resistance_level = resistance_level

    def check_signal(self, positions):
        mt5_api.initialize()
        current_price = mt5_api.get_current_price(self.symbol)

        if current_price < self.support_level:
            return "buy"
        elif current_price > self.resistance_level:
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

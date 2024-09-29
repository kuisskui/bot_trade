import mt5_api
from indicator import get_bollinger_bands
from datetime import datetime


class BollingerBandsStrategy:
    def __init__(self, symbol, time_frame=mt5_api.TIMEFRAME_M1, lot=0.01, period=20, std_dev=2):
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.period = period
        self.std_dev = std_dev

        self.signal = ""
        self.positions = None
        self.upper_band = None
        self.middle_band = None
        self.lower_band = None
        self.current_price = None

    def check_signal(self):
        mt5_api.initialize()
        self.positions = mt5_api.positions_get(symbol=self.symbol)
        self.upper_band, self.lower_band, self.middle_band = get_bollinger_bands(self.symbol, self.time_frame, self.period, self.std_dev)
        self.current_price = mt5_api.symbol_info_tick(self.symbol).bid

        if self.positions:
            if self.positions[0].type is mt5_api.POSITION_TYPE_BUY:
                if self.current_price >= self.middle_band:
                    self.signal = "exit"
                else:
                    self.signal = "hold"
            elif self.positions[0].type is mt5_api.POSITION_TYPE_SELL:
                if self.current_price <= self.middle_band:
                    self.signal = "exit"
                else:
                    self.signal = "hold"
        else:
            if self.current_price <= self.lower_band:
                self.signal = "buy"
            elif self.current_price >= self.upper_band:
                self.signal = "sell"
            else:
                self.signal = "hold"

    def send_order(self):
        if self.signal == "buy":
            mt5_api.place_trade(self.symbol, self.lot, "buy")
        elif self.signal == "sell":
            mt5_api.place_trade(self.symbol, self.lot, "sell")
        elif self.signal == "exit":
            mt5_api.close_position(self.positions[0])

        self.positions = mt5_api.positions_get(symbol=self.symbol)

    def report(self):
        report_string = f"""
[{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}]
Strategy: {type(self).__name__}
Symbol: {self.symbol}
Current Price: {self.current_price}
Upper Band: {self.upper_band}
Middle Band: {self.middle_band}
Lower Band: {self.lower_band}
Signal: {self.signal}
"""
        if self.positions:
            position_string = f"""
Position: Type: {"BUY" if self.positions[0].type is mt5_api.POSITION_TYPE_BUY else "SELL"}
        : Ticket: {self.positions[0].ticket}
        """
        else:
            position_string = """
Position: -
            """
        print(report_string, position_string)
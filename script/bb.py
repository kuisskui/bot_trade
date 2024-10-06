import mt5_api
from script.indicator import get_bollinger_bands
from datetime import datetime


class BollingerBandsStrategy:
    def __init__(self, symbol, time_frame=mt5_api.TIMEFRAME_M1, lot=0.01, period=20, std_dev=2):
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.period = period
        self.std_dev = std_dev

        self.signal = ""
        self.position = None
        self.upper_band = None
        self.middle_band = None
        self.lower_band = None
        self.current_price = None

    def check_signal(self):
        mt5_api.initialize()
        self.position = mt5_api.positions_get(symbol=self.symbol)
        self.upper_band, self.middle_band, self.lower_band = get_bollinger_bands(self.symbol, self.time_frame, 0, self.period, self.std_dev)
        self.current_price = mt5_api.symbol_info_tick(self.symbol).bid

        if self.position:
            if self.position[0].type is mt5_api.POSITION_TYPE_BUY:
                if self.current_price >= self.upper_band:
                    self.signal = "sell"
                else:
                    self.signal = "hold"
            elif self.position[0].type is mt5_api.POSITION_TYPE_SELL:
                if self.current_price <= self.lower_band:
                    self.signal = "buy"
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
            if self.position:
                mt5_api.close_position(self.position[0])
            mt5_api.place_trade(self.symbol, self.lot, "buy")
        elif self.signal == "sell":
            if self.position:
                mt5_api.close_position(self.position[0])
            mt5_api.place_trade(self.symbol, self.lot, "sell")
        elif self.signal == "exit":
            mt5_api.close_position(self.position[0])

        self.position = mt5_api.positions_get(symbol=self.symbol)

    def report(self):
        datetime_string = f"[{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}]"
        strategy_string = f"Strategy: {type(self).__name__}"
        symbol_string = f"Symbol: {self.symbol}"
        current_price_string = f"Current Price: {self.current_price}"
        upper_band_string = f"Upper Band: {self.upper_band}"
        middle_band_string = f"Middle Band: {self.middle_band}"
        lower_band_string = f"Lower Band: {self.lower_band}"
        signal_string = f"Signal: {self.signal}"

        if self.position:
            position_string = f"Position: Type {"BUY" if self.position[0].type is mt5_api.POSITION_TYPE_BUY else "SELL"}"
            ticket_string =   f"        : Ticket {self.position[0].ticket}"
        else:
            position_string = "Position: No position"
            ticket_string = ""

        print(f"""
{datetime_string}
{strategy_string}
{symbol_string}
{current_price_string}
{upper_band_string}
{middle_band_string}
{lower_band_string}
{signal_string}
{position_string}
{ticket_string}
                        """)

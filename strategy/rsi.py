import mt5_api
from datetime import datetime

from strategy.strategy import Strategy
from indicator import get_relative_strength_index


class RSIStrategy(Strategy):
    def __init__(self, symbol, time_frame=mt5_api.TIMEFRAME_M1, lot=0.01, overbought=70, oversold=30):
        super().__init__()
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.overbought = overbought
        self.oversold = oversold

        self.signal = ""
        self.positions = None
        self.rsi = 0

    def check_signal(self):
        mt5_api.initialize()
        self.positions = mt5_api.positions_get(symbol=self.symbol)
        self.rsi = get_relative_strength_index(self.symbol, self.time_frame, 0, 14)

        if self.positions:
            if self.positions[0].type is mt5_api.POSITION_TYPE_SELL:
                if self.rsi <= self.oversold:
                    self.signal = "buy"
                else:
                    self.signal = "hold"
            elif self.positions[0].type is mt5_api.POSITION_TYPE_BUY:
                if self.rsi >= self.overbought:
                    self.signal = "sell"
                else:
                    self.signal = "hold"
        else:
            if self.rsi >= self.overbought:
                self.signal = "sell"
            elif self.rsi <= self.oversold:
                self.signal = "buy"
            else:
                self.signal = "hold"

    def send_order(self):
        if self.signal == "buy":
            if self.positions:
                mt5_api.close_position(self.positions[0])
            mt5_api.place_trade(self.symbol, self.lot, "buy")
        elif self.signal == "sell":
            if self.positions:
                mt5_api.close_position(self.positions[0])
            mt5_api.place_trade(self.symbol, self.lot, "sell")
        elif self.signal == "exit":
            mt5_api.close_position(self.positions[0])
        self.positions = mt5_api.positions_get(symbol=self.symbol)

    def report(self):
        datetime_string = f"[{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}]"
        strategy_string = f"Strategy: {type(self).__name__}"
        symbol_string = f"Symbol: {self.symbol}"
        RSI_string = f"RSI: {self.rsi}"
        signal_string = f"Signal: {self.signal}"
        if self.positions:
            position_string = f"Position: Type {"BUY" if self.positions[0].type is mt5_api.POSITION_TYPE_BUY else "SELL"}"
            tick_string =     f"        : Ticket {self.positions[0].ticket}"
        else:
            position_string = "Position: No position"
            tick_string = ""

        print(f"""
{datetime_string}
{strategy_string}
{symbol_string}
{RSI_string}
{signal_string}
{position_string}
{tick_string}
                """)

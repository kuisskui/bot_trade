import mt5_api
from datetime import datetime
from indicator import get_relative_strength_index


class RSIStrategy:
    def __init__(self, symbol, time_frame=mt5_api.TIMEFRAME_M1, lot=0.01, overbought=70, oversold=30):
        mt5_api.initialize()
        self.signal = ""
        self.positions = mt5_api.positions_get(symbol=symbol)
        self.symbol = symbol
        self.time_frame = time_frame
        self.lot = lot
        self.overbought = overbought
        self.oversold = oversold
        self.rsi = 0

    def check_signal(self):
        # this strategy might check and return hold until the port is broken if the market is dum to a way
        mt5_api.initialize()
        self.rsi = get_relative_strength_index(self.symbol, self.time_frame, 0, 14)

        if self.positions:
            if self.positions[0].type == mt5_api.POSITION_TYPE_SELL:
                if self.rsi <= 50:
                    self.signal = "exit"
                else:
                    self.signal = "hold"
            elif self.positions[0].type == mt5_api.POSITION_TYPE_BUY:
                if self.rsi >= 50:
                    self.signal = "exit"
                else:
                    self.signal = "hold"
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
            if not self.positions:
                mt5_api.place_trade(self.symbol, self.lot, "buy")

            elif self.positions[0].type == 1:
                mt5_api.close_position(self.positions[0])
                mt5_api.place_trade(self.symbol, self.lot, "buy")

        elif self.signal == "sell":
            if not self.positions:
                mt5_api.place_trade(self.symbol, self.lot, "sell")
            elif self.positions[0].type == 0:
                mt5_api.close_position(self.positions[0])
                mt5_api.place_trade(self.symbol, self.lot, "sell")

        elif self.signal == "exit":
            if self.positions:
                mt5_api.close_position(self.positions[0])

        self.positions = mt5_api.positions_get(symbol=self.symbol)

    def report(self):
        print(f"""
[{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}]
Strategy: {type(self).__name__}
Symbol: {self.symbol}
RSI: {self.rsi}
Signal: {self.signal}
Position: {self.positions[0].ticket if self.positions else "No position"}
        """)

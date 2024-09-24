import mt5_api
from exception import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime


class Strategy:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.previous_short_ma = None
        self.previous_long_ma = None

    def start(self):
        symbol = "USOIL"
        timeframe = mt5_api.TIMEFRAME_M1
        lot = 0.1
        short_period = 10
        long_period = 50
        trigger = CronTrigger(second=0)

        trigger_debug = IntervalTrigger(seconds=3)

        self.scheduler.start()
        self.ma_crossing_trade(symbol, timeframe, lot, short_period, long_period)
        self.scheduler.add_job(
            self.ma_crossing_trade,
            kwargs={
                "symbol": symbol,
                "time_frame": timeframe,
                "lot": lot,
                "short_period": short_period,
                "long_period": long_period,
            },
            trigger=trigger
        )
        print("schedule start")

    def stop(self):
        self.scheduler.shutdown()
        self.shutdown()

    def initialize(self):
        if not mt5_api.initialize():
            raise InitializationException('mt5_api initialization failed')

    def shutdown(self):
        mt5_api.shutdown()

    def ma_crossing_trade(self, symbol, time_frame, lot, short_period, long_period):
        self.initialize()

        print(f"-----KuiBot: trade is called: [{datetime.now()}]-----")

        current_short_ma = mt5_api.get_moving_average(symbol, time_frame, short_period)
        current_long_ma = mt5_api.get_moving_average(symbol, time_frame, long_period)

        # If this is the first run, store the MAs and return (no crossover check yet)
        if self.previous_short_ma is None or self.previous_long_ma is None:
            self.previous_short_ma = current_short_ma
            self.previous_long_ma = current_long_ma
            print("KuiBot: set ma")
            return True

        crossed_up = self.previous_short_ma <= self.previous_long_ma and current_short_ma > current_long_ma
        crossed_down = self.previous_short_ma >= self.previous_long_ma and current_short_ma < current_long_ma

        print(f"MA crossing check: crossed_up={crossed_up}, crossed_down={crossed_down}")
        is_uptrend = current_short_ma > current_long_ma
        if is_uptrend:
            print("Current trend: UP")
        else:
            print("Current trend: DOWN")

        if crossed_up:
            # Bullish crossover: Buy signal
            print("Bullish crossover detected (Buy signal)")
            active_positions = mt5_api.positions_get(symbol=symbol)
            if not active_positions:
                mt5_api.place_trade(symbol, lot, "buy", deviation=100)

            elif active_positions[0].type == 1:
                mt5_api.close_all_orders()
                mt5_api.place_trade(symbol, lot, "buy", deviation=100)

        elif crossed_down:
            # Bearish crossover: Sell signal
            print("Bearish crossover detected (Sell signal)")
            active_positions = mt5_api.positions_get(symbol=symbol)
            if not active_positions:
                mt5_api.place_trade(symbol, lot, "sell", deviation=100)
            elif active_positions[0].type == 0:
                mt5_api.close_all_orders()
                mt5_api.place_trade(symbol, lot, "sell", deviation=100)

        self.previous_short_ma = current_short_ma
        self.previous_long_ma = current_long_ma

        self.shutdown()

    def rsi_trade(self, symbol, time_frame, lot, overbought, oversold):
        self.initialize()
        print(f"-----KuiBot: trade is called: [{datetime.now()}]-----")
        rsi = mt5_api.get_relative_strength_index(symbol, time_frame)
        print(f"RSI percentage: {rsi}%")
        if rsi > overbought:
            print("RSI is overbought")
            mt5_api.place_trade(symbol, lot, "sell", deviation=100)
        if rsi < oversold:
            print("RSI is oversold")
            mt5_api.place_trade(symbol, lot, "buy", deviation=100)
        self.shutdown()


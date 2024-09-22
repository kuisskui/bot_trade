import mt5_api as mt5
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
        trigger = CronTrigger(second=0)
        trigger_debug = IntervalTrigger(seconds=3)
        self.scheduler.start()
        self.ma_crossing_trade()
        self.scheduler.add_job(
            self.ma_crossing_trade,
            kwargs={
                "symbol": "BTCUSD",
                "time_frame": mt5.TIMEFRAME_M1,
                "lot": 0.1,
                "short_period": 10,
                "long_period": 50,
            },
            trigger=trigger
        )
        print("schedule start")

    def initialize(self):
        if not mt5.initialize():
            raise InitializationException('mt5 initialization failed')

    def shutdown(self):
        mt5.shutdown()

    def ma_crossing_trade(self, symbol, time_frame, lot, short_period, long_period):
        self.initialize()

        print(f"-----KuiBot: trade is called: [{datetime.now()}]-----")

        current_short_ma = mt5.get_moving_average(symbol, time_frame, short_period)
        current_long_ma = mt5.get_moving_average(symbol, time_frame, long_period)

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
            active_positions = mt5.get_active_positions(symbol)
            if not active_positions:
                mt5.place_trade(symbol, lot, "buy")

            elif active_positions[0].type == 1:
                mt5.close_all_orders()
                mt5.place_trade(symbol, lot, "buy")

        elif crossed_down:
            # Bearish crossover: Sell signal
            print("Bearish crossover detected (Sell signal)")
            active_positions = mt5.get_active_positions(symbol)
            if not active_positions:
                mt5.place_trade(symbol, lot, "sell")
            elif active_positions[0].type == 0:
                mt5.close_all_orders()
                mt5.place_trade(symbol, lot, "sell")

        self.previous_short_ma = current_short_ma
        self.previous_long_ma = current_long_ma

        self.shutdown()

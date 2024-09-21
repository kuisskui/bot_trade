import mt5_api
from apscheduler.triggers.interval import IntervalTrigger
import time
import MetaTrader5 as mt5


class Bot:
    def __init__(self, account_id, password, server, scheduler):
        self.account_id = account_id
        self.password = password
        self.server = server
        self.scheduler = scheduler

    def start(self):
        print('Bot: start is called')

        self.connect_to_mt5()
        self.scheduler.start()
        print("Bot: Succeeded to start scheduler")

        self.scheduler.add_job(
            self.task,
            trigger=IntervalTrigger(seconds=60),
        )
        print("Bot: Succeeded to add job")

    def stop(self):
        print('Bot: stop is called')

        self.scheduler.shutdown()
        print("Bot: Succeeded to shutdown scheduler")

        mt5_api.shutdown_mt5()
        print("Bot: Succeeded to shutdown MetaTrader 5")

    def connect_to_mt5(self, attempt_limit=5):
        print("Bot: connect_to_mt5 is called")

        if attempt_limit == 0:
            print("Bot: Failed to connect to MetaTrader 5 after reaching attempt limit")
            return

        if mt5_api.initialize_mt5(self.account_id, self.password, self.server):
            print("Bot: Connected to MetaTrader 5 successfully")
        else:
            print(f"Bot: Failed to connect, retrying... (Attempts left: {attempt_limit - 1})")
            self.connect_to_mt5(attempt_limit - 1)

    def task(self):
        symbol = "BTCUSD"
        lot = 0.01
        print("Bot: task is called")
        current = mt5_api.iMA(symbol, mt5.TIMEFRAME_M1, 14,0)
        previous = mt5_api.iMA(symbol, mt5.TIMEFRAME_M1, 14, 1)
        # print("=====================================")
        # print(time.time())
        # print("current MA14")
        # print(current)
        # print("=====================================")
        # print("previous MA14")
        # print(previous)
        # print("=====================================")
        # print(mt5_api.orders_get())
        if current < previous:
            if mt5_api.get_active_positions(symbol)[0].type == 1:
                mt5_api.close_all_orders()
                mt5_api.place_trade(symbol, lot,"buy")
        else:
            if mt5_api.get_active_positions(symbol)[0].type == 0:
                mt5_api.close_all_orders()
                mt5_api.place_trade(symbol, lot,"sell")


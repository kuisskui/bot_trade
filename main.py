from fastapi import FastAPI
from PythonMetaTrader5 import *
from strategy import BollingerBandsStrategy, RSIStrategy
from dotenv import load_dotenv
from bot.bot_manager import BotManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import uvicorn
import os
import pytz

load_dotenv()

app = FastAPI()
account_id = 176471571
password = os.getenv("password")
server = "Exness-MT5Trial7"
bot_manager: BotManager = BotManager()
scheduler: AsyncIOScheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    print("fastapi: startup_event")
    scheduler.start()
    await trade_test_rsi_major_pair()


@app.get(path="/bots")
def get_bots():
    return bot_manager.bots


async def trade_rsi_major_pair():
    print("Start trade")
    thai_timezone = pytz.timezone('Asia/Bangkok')
    eurusd_bot = bot_manager.create_new_bot(RSIStrategy("EURUSD"))
    scheduler.add_job(
        eurusd_bot.trade,
        trigger=CronTrigger(minute='*', hour='4-13', day_of_week='mon-fri', timezone=thai_timezone)
    )

    usdjpy_bot = bot_manager.create_new_bot(RSIStrategy("USDJPY"))
    scheduler.add_job(
        usdjpy_bot.trade,
        trigger=CronTrigger(minute='*', hour='4-6, 16-18', day_of_week='mon-fri', timezone=thai_timezone)
    )

    gbpusd_bot = bot_manager.create_new_bot(RSIStrategy("GBPUSD"))
    scheduler.add_job(
        gbpusd_bot.trade,
        trigger=CronTrigger(minute='*', hour='4-14', day_of_week='mon-fri', timezone=thai_timezone)
    )

    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("USDCHF"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*', hour='4-12', day_of_week='mon-fri', timezone=thai_timezone)
    )


async def trade_test_rsi_major_pair():
    print("Start test: trade_test_rsi_major_pair")
    BTCUSD = bot_manager.create_new_bot(RSIStrategy("BTCUSD"))
    scheduler.add_job(
        BTCUSD.trade,
        trigger=CronTrigger(second='*/5'),
        replace_existing=True
    )
    BTCJPY = bot_manager.create_new_bot(BollingerBandsStrategy("BTCJPY"))
    scheduler.add_job(
        BTCJPY.trade,
        trigger=CronTrigger(second='*/5'),
        replace_existing=True
    )
    # BTCXAU = bot_manager.create_new_bot(BollingerBandsStrategy("BTCXAU"))
    # scheduler.add_job(
    #     BTCXAU.trade,
    #     trigger=CronTrigger(second='*/5'),
    #     replace_existing=True
    # )


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    bot_manager.stop()
    print("fastapi: shutdown_event")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

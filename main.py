from fastapi import FastAPI
from PythonMetaTrader5 import *
from strategy import MovingAverageCrossingOverStrategy, RSIStrategy, ExponentialMovingAverageCrossingOverStrategy
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


@app.get(path="/bots")
def get_bots():
    return bot_manager.bots


@app.post(path="/bots/trade/ma")
async def trade_ma():
    bot = bot_manager.create_new_bot(MovingAverageCrossingOverStrategy("USOIL"))
    bot.trade()
    scheduler.add_job(
        bot.trade,
        trigger=CronTrigger(second=0)
    )
    return bot


@app.post(path="/bots/trade/ema")
async def trade_ema():
    bot = bot_manager.create_new_bot(ExponentialMovingAverageCrossingOverStrategy("BTCUSD"))
    bot.trade()
    scheduler.add_job(
        bot.trade,
        trigger=CronTrigger(second=0)
    )


@app.post(path="/bots/trade/rsi")
async def trade_rsi():
    bot = bot_manager.create_new_bot(RSIStrategy("BTCUSD"))
    bot.trade()
    scheduler.add_job(
        bot.trade,
        trigger=CronTrigger(second=0)
    )
    return bot


@app.post(path="/bots/trade/rsi/major-pair")
async def trade_rsi_major_pair():
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

@app.post(path="/bots/trade/test")
async def trade_rsi_major_pair():
    eurusd_bot = bot_manager.create_new_bot(RSIStrategy("BTCUSD"))
    scheduler.add_job(
        eurusd_bot.trade,
        trigger=CronTrigger(minute='*')
    )

    usdjpy_bot = bot_manager.create_new_bot(RSIStrategy("ETHUSD"))
    scheduler.add_job(
        usdjpy_bot.trade,
        trigger=CronTrigger(minute='*')
    )

    gbpusd_bot = bot_manager.create_new_bot(RSIStrategy("LTCUSD"))
    scheduler.add_job(
        gbpusd_bot.trade,
        trigger=CronTrigger(minute='*')
    )

    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("BTCZAR"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )
    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("BTCTHB"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )
    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("BTCJPY"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )
    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("BTCXAU"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )
    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("BTCAUD"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )
    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("BTCCNH"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )
    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("BTCXAG"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )
    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("DOGEUSD"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )
    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("IOSTUSD"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )
    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("XRPUSD"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )

    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("BCHUSD"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )

    usdchf_bot = bot_manager.create_new_bot(RSIStrategy("BTCKRW"))
    scheduler.add_job(
        usdchf_bot.trade,
        trigger=CronTrigger(minute='*')
    )


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    bot_manager.stop()
    print("fastapi: shutdown_event")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

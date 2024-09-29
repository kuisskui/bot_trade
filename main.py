from fastapi import FastAPI
from PythonMetaTrader5 import *
from strategy import MovingAverageCrossingOverStrategy, RSIStrategy, ExponentialMovingAverageCrossingOverStrategy
from dotenv import load_dotenv
from bot.bot_manager import BotManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import uvicorn
import os

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
    return bot_manager


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


@app.post(path="/bots/backtest/ma")
async def backtest_ma():
    bot = bot_manager.create_new_bot(MovingAverageCrossingOverStrategy("EURUSD"))


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    bot_manager.stop()
    print("fastapi: shutdown_event")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

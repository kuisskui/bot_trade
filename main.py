from fastapi import FastAPI
from PythonMetaTrader5 import *
from dotenv import load_dotenv
from bot.manager import BotManager
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


@app.post(path="/bots/trade")
async def trade():
    bot = bot_manager.create_new_bot()

    scheduler.add_job(
        bot.trade,
        trigger=CronTrigger(second=0)
    )
    return bot


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    bot_manager.stop()
    print("fastapi: shutdown_event")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

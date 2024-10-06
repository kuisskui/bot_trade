import os
import pytz
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bot.bot_manager import bot_manager
from strategy import RSIStrategy
from ws import ws

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or specify a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(ws.router)

account_id = 176471571  # Your account number
password = os.getenv("password")  # Your MetaTrader password
server = "Exness-MT5Trial7"  # The server for your account

scheduler: AsyncIOScheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    scheduler.start()
    await trade_rsi_major_pair()


@app.get(path="/bots")
def get_bots():
    return bot_manager.bots


async def trade_test():
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


async def trade_rsi_major_pair():
    UTC_timezone = pytz.timezone('UTC')
    BTCUSD = bot_manager.create_new_bot(RSIStrategy("BTCUSD"))
    scheduler.add_job(
        BTCUSD.trade,
        trigger=CronTrigger(day_of_week="*", minute="*", timezone=UTC_timezone),
        replace_existing=True
    )
    BTCJPY = bot_manager.create_new_bot(RSIStrategy("BTCJPY"))
    scheduler.add_job(
        BTCJPY.trade,
        trigger=CronTrigger(day_of_week="*", minute="*", timezone=UTC_timezone),
        replace_existing=True
    )
    BTCXAU = bot_manager.create_new_bot(RSIStrategy("BTCXAU"))
    scheduler.add_job(
        BTCXAU.trade,
        trigger=CronTrigger(day_of_week="*", minute="*", timezone=UTC_timezone),
        replace_existing=True
    )


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

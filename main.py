import os
import pytz
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strategy.router import strategy_router
import bot
from bot.bot_manager import bot_manager
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
app.include_router(strategy_router)

account_id = 176471571  # Your account number
password = os.getenv("password")  # Your MetaTrader password
server = "Exness-MT5Trial7"  # The server for your account

scheduler: AsyncIOScheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    scheduler.start()


@app.get(path="/bots")
def get_bots():
    return bot_manager.bots


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

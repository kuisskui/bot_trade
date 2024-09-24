from fastapi import FastAPI
from PythonMetaTrader5 import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from bot import Bot
from strategy import Strategy
import uvicorn
import os
import asyncio

load_dotenv()

app = FastAPI()
account_id = 176471571  # Your account number
password = os.getenv("password")  # Your MetaTrader password
server = "Exness-MT5Trial7"  # The server for your account
strategy = Strategy()
bot = Bot(strategy)
bots = []
broker = Broker(account_id, password, server)


@app.on_event("startup")
async def startup_event():
    print("fastapi: startup_event")

    print("fastapi: call bot start")
    try:
        bot.start()
        print("fastapi: bot started")
    except Exception as e:
        print(e)
        bot.stop()
        await shutdown_event()


@app.get(path="/bots")
def get_bots():
    return f"All bots {bots}"


@app.post(path="/bots/trade")
async def trade(e):
    bot = Bot(strategy)
    bot.start()
    bots.append(bot)


@app.on_event("shutdown")
async def shutdown_event():
    print("fastapi: shutdown_event")

    print("fastapi: call bot stop")
    bot.stop()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

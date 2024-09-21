from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from bot import Bot
import uvicorn
import os
import asyncio

load_dotenv()

app = FastAPI()
scheduler = AsyncIOScheduler()
account_id = 176471571  # Your account number
password = os.getenv("password")  # Your MetaTrader password
server = "Exness-MT5Trial7"  # The server for your account
bot = Bot(account_id, password, server, scheduler)


@app.on_event("startup")
async def startup_event():
    print("fastapi: startup")

    print("fastapi: call bot start")
    bot.start()


@app.on_event("shutdown")
async def shutdown_event():
    print("fastapi: shutdown")

    print("fastapi: call bot stop")
    bot.stop()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

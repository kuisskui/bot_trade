from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import load_dotenv
import uvicorn
import logging
import mt5_api
import os
import asyncio

load_dotenv()

app = FastAPI()

scheduler = AsyncIOScheduler()


def scheduled_trade_task():
    logging.info("Scheduled task: Checking market and placing trade if conditions are met")
    mt5_api.place_trade("EURUSD", 0.01, "buy")
    logging.info("Trade placed successfully")


@app.on_event("startup")
async def startup_event():
    account_id = 176471571  # Your account number
    password = os.getenv("password")  # Your MetaTrader password
    server = "Exness-MT5Trial7"  # The server for your account
    if mt5_api.initialize_mt5(account_id, password, server):
        print("Connected to MetaTrader 5 successfully")
    else:
        print("Failed to connect to MetaTrader 5")

    # Start the scheduler and add the scheduled job
    scheduler.start()
    print("Succeed to start schedular")

    # Schedule the task to run every 5 minutes
    # scheduler.add_job(
    #     scheduled_trade_task,
    #     trigger=IntervalTrigger(seconds=5),
    # )
    # print("Succeed to add job")


@app.get("/trade")
async def trade():
    try:
        # Execute the trade task in a non-blocking way
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, scheduled_trade_task)
        return {"status": "accepted", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.on_event("shutdown")
async def shutdown_event():
    mt5_api.shutdown_mt5()
    print("Succeed to shutdown MetaTrader 5 successfully")
    scheduler.shutdown()
    print("Succeed to shutdown schedular")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

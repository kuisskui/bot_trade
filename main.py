from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import uvicorn
import logging
import mt5_api
app = FastAPI()

scheduler = AsyncIOScheduler()


def scheduled_trade_task(sting):
    logging.info("Scheduled task: Checking market and placing trade if conditions are met")
    mt5_api.place_trade("EURUSD", 0.1, "buy")
    logging.info("Trade placed successfully")


@app.on_event("startup")
async def startup_event():
    account_id = 12345678  # Your account number
    password = "password"  # Your MetaTrader password
    server = "YourServer"  # The server for your account
    if mt5_api.initialize_mt5(account_id, password, server):
        logging.info("Connected to MetaTrader 5 successfully")
    else:
        logging.error("Failed to connect to MetaTrader 5")

    # Start the scheduler and add the scheduled job
    scheduler.start()

    # Schedule the task to run every 5 minutes
    scheduler.add_job(
        scheduled_trade_task,
        trigger=IntervalTrigger(minutes=5),
        id="trading_task",  # Optional: ID for the scheduled task
        replace_existing=True  # Replace the task if it already exists
    )


@app.on_event("shutdown")
async def shutdown_event():
    mt5_api.shutdown_mt5()
    scheduler.shutdown()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

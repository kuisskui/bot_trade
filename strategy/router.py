from asyncio import sleep

from fastapi import APIRouter, WebSocket, Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from strategy.strategy import Strategy

from strategy.strategy_manager import strategy_manager

strategy_router = APIRouter(prefix="/strategies")


@strategy_router.get("/")
async def get_strategies():
    return [s.split('.')[0] for s in strategy_manager.get_all_strategies()]


@strategy_router.get("/active")
async def get_strategies():
    return [(s.script, s.signal) for s in strategy_manager.get_active_strategies()]


@strategy_router.post("/run")
async def post_strategies(request: Request):
    state = await request.json()

    try:
        script = state.get("script")
        trigger_data = state.get("trigger")
        print("debug: ")
        print(type(trigger_data))
        print(trigger_data)

        if not script or not trigger_data:
            return {"status": 400, "message": "Missing 'script' or 'trigger' in the request."}

        cron_trigger = CronTrigger(**trigger_data)

        s = Strategy(script, state)

        scheduler = AsyncIOScheduler()
        scheduler.start()
        scheduler.add_job(
            s.get_signal,
            trigger=cron_trigger
        )

        strategy_manager.add_strategy(s)
        return {"status": 200, "state": state}

    except Exception as e:
        return {"status": 500, "message": str(e)}


@strategy_router.websocket("/ws")
async def strategy(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            await sleep(1)
            await websocket.send_text("Strategy interface")
    except Exception as e:
        print(e)

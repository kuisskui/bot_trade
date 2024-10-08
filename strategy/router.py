from asyncio import sleep

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, WebSocket, Request

from strategy.strategy_manager import strategy_manager
from bot.bot_manager import bot_manager

strategy_router = APIRouter(prefix="/strategies")


@strategy_router.get("/")
async def get_strategies():
    return [s.split('.')[0] for s in strategy_manager.get_all_strategies()]


@strategy_router.get("/active")
async def get_strategies():
    return [(s.strategy_id, s.script, s.signal) for s in strategy_manager.get_active_strategies()]


@strategy_router.post("/run")
async def post_strategies(request: Request):
    state = await request.json()

    try:
        script = state.get("script")
        trigger_data = state.get("trigger")

        if not script or not trigger_data:
            return {"status": 400, "message": "Missing 'script' or 'trigger' in the request."}

        cron_trigger = CronTrigger(**trigger_data)

        s = strategy_manager.run_new_strategy(script, state)

        scheduler = AsyncIOScheduler()
        scheduler.start()
        scheduler.add_job(
            s.get_signal,
            trigger=cron_trigger
        )

        return {"status": 200, "message": "run successfully"}

    except Exception as e:
        return {"status": 500, "message": str(e)}


@strategy_router.post("/subscribe")
async def follow_trade_strategy(request: Request):
    state = await request.json()
    strategy_id = state.get('strategy_id')
    bot = bot_manager.create_new_bot()
    strategy = strategy_manager.get_strategy_by_id(strategy_id)
    strategy.subscribe(bot)
    return {"status": 200, "message": "subscribe successfully"}


@strategy_router.websocket("/ws")
async def strategy(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            await sleep(1)
            await websocket.send_text("Strategy interface")
    except Exception as e:
        print(e)

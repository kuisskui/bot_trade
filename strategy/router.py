from asyncio import sleep

from fastapi import APIRouter, WebSocket, Request

from bot.bot_manager import bot_manager
from strategy.strategy_manager import strategy_manager

strategy_router = APIRouter(prefix="/strategies")


@strategy_router.get("/")
async def get_strategies():
    return [s.split('.')[0] for s in strategy_manager.get_all_strategies()]


@strategy_router.get("/active")
async def get_active_strategies():
    return [(s.strategy_id, s.script, s.signal) for s in strategy_manager.get_active_strategies()]


@strategy_router.post("/run")
async def run_strategies(request: Request):
    try:
        state = await request.json()

        symbol = state.get("symbol")
        script = state.get("script")
        trigger = state.get("trigger")

        if not script or not trigger or not symbol:
            return {"status": 400, "message": "Missing 'symbol', 'script' or 'trigger' in the request."}

        strategy_manager.run_new_strategy(script, trigger, state)

        return {"status": 200, "message": "run successfully"}
    except Exception as e:
        return {"status": 500, "message": str(e)}


@strategy_router.post("/subscribe")
async def subscribe_strategy(request: Request):
    try:
        state = await request.json()

        strategy_id = state.get('strategy_id')

        if not strategy_id:
            return {"status": 400, "message": "Missing 'strategy_id' in the request."}

        bot = bot_manager.create_new_bot()

        strategy = strategy_manager.get_strategy_by_id(strategy_id)

        strategy.subscribe(bot)

        return {"status": 200, "message": "subscribe successfully"}
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

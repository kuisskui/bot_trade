from asyncio import sleep

from fastapi import APIRouter, WebSocket

from strategy.strategy import Strategy

from strategy.strategy_manager import strategy_manager

strategy_router = APIRouter(prefix="/strategies")


@strategy_router.get("/")
async def get_strategies():
    return [s.split('.')[0] for s in strategy_manager.get_all_strategies()]


@strategy_router.post("/run")
async def post_strategies():
    strategy_manager.add_strategy(Strategy('rsi.py'))
    return {"status": 200}


@strategy_router.get("/run")
async def run_strategy():
    return strategy_manager.get_active_strategies()[0].get_signal()


@strategy_router.websocket("/ws")
async def strategy(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            await sleep(1)
            await websocket.send_text("Strategy interface")
    except Exception as e:
        print(e)

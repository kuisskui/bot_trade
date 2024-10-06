from asyncio import sleep

from fastapi import APIRouter, WebSocket

from strategy.strategy import Strategy

strategy_router = APIRouter(prefix="/strategies")


@strategy_router.get("/")
async def root():
    strategy = Strategy('rsi.py')
    return {"strategy": strategy.get_signal(), "script": strategy.script}


@strategy_router.websocket("/strategies")
async def strategy(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            await sleep(1)
            await websocket.send_text("Strategy interface")
    except Exception as e:
        print(e)

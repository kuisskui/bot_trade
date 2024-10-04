import json
import random
from typing import List
from fastapi import APIRouter, WebSocket
from asyncio import sleep
from starlette.websockets import WebSocketDisconnect
from ws.web_socket import websocket_manager
from bot.bot_model import BotDTO, StrategyDTO
from bot.bot_manager import bot_manager

router = APIRouter(prefix="/ws")


@router.get("/test")
async def test():
    return "test"


@router.websocket("/live")
async def live(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            await sleep(1)
            bots = bot_manager.get_bots()
            message = []
            for bot in bots:
                strategy = bot.strategy
                strategy_dto = StrategyDTO(
                    symbol=strategy.symbol,
                    time_frame=strategy.time_frame,
                    lot=strategy.lot,
                    signal=strategy.signal,
                    position="Buy" if strategy.position[0].type == 0 else "Sell",
                )
                bot_dto = BotDTO(
                    bot_id=bot.bot_id,
                    strategy=strategy_dto
                )
                message.append(bot_dto)
            await websocket.send_text(json.dumps([bot.dict() for bot in message]))
    except Exception as e:
        print(e)

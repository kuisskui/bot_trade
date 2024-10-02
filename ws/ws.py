import json
import random
from typing import List
from fastapi import APIRouter, WebSocket
from asyncio import sleep
from starlette.websockets import WebSocketDisconnect
from ws.web_socket import websocket_manager
from bot.bot_model import BotDTO, PositionDTO

router = APIRouter(prefix="/ws")

bots: List[BotDTO] = [
    BotDTO(
        name="BTCUSD-RSI Bot Trading",
        positions=[PositionDTO(type="buy", profit=12), PositionDTO(type="sell", profit=-2)],
        online=True
    ),
    BotDTO(
        name="BTCJPY-Bollinger Band Bot Trading",
        positions=[PositionDTO(type="buy", profit=12), PositionDTO(type="sell", profit=-2)],
        online=True
    )
]


@router.get("/test")
async def test():
    return "test"


@router.websocket("/live")
async def live(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            await sleep(1)
            message = []
            for bot in bots:
                positions = []
                for position in bot.positions:
                    position_dto = PositionDTO(
                        type=position.type,
                        profit=random.randint(1, 10)
                    )
                    positions.append(position_dto)
                bot_dto = BotDTO(
                    name=bot.name,
                    online=bot.online,
                    positions=positions
                )
                message.append(bot_dto)
            await websocket.send_text(json.dumps([bot.dict() for bot in message]))
    except Exception as e:
        print(e)

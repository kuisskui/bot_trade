import json
from asyncio import sleep

from fastapi import APIRouter, WebSocket

from bot.bot_manager import bot_manager
from bot.bot_model import BotDTO, StrategyDTO

bot_router = APIRouter(prefix="/bots")


@bot_router.get("/")
async def get_bots():
    return bot_manager.get_bots()

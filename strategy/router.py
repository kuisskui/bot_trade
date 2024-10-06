from fastapi import APIRouter
from strategy.strategy import Strategy


strategy_router = APIRouter(prefix="/strategies")


@strategy_router.get("/")
async def root():
    strategy = Strategy('rsi.py')
    return {"strategy": strategy.get_signal(), "script": strategy.script}
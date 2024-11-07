from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from bot.bot_manager import bot_manager
from strategy.strategy_manager import strategy_manager
from fastapi.responses import JSONResponse
from pathlib import Path
import os

strategy_router = APIRouter(prefix="/strategies")
BASE_DIR = Path(os.getenv("BASE_DIR"))
SCRIPT_DIR = BASE_DIR / os.getenv("SCRIPT_DIR")


@strategy_router.get("/all")
async def get_strategies():
    return [s.split('.')[0] for s in strategy_manager.get_all_strategies()]


@strategy_router.get("/active")
async def get_active_strategies():
    return [s.__dict__ for s in strategy_manager.get_active_strategies()]


@strategy_router.post("/save_strategy")
async def save_strategy(file: UploadFile = File(...)):
    if not file.filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="File must be a Python (.py) file.")

    try:
        os.makedirs(os.path.dirname(SCRIPT_DIR), exist_ok=True)

        file_location = os.path.join(SCRIPT_DIR, file.filename)

        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        return JSONResponse(content={"message": "File saved successfully", "file_path": file_location})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")


@strategy_router.post("/run")
async def run_strategies(request: Request):
    try:
        state = await request.json()

        symbol = state.get("symbol")
        script = state.get("script")
        trigger = state.get("trigger")

        if not script or not symbol or not trigger:
            return {"status": 400, "message": "Missing 'symbol', 'script' or 'trigger' in the request."}

        strategy_manager.run_new_strategy(state)

        return {"status": 200, "message": "run successfully"}
    except Exception as e:
        return {"status": 500, "message": str(e)}


@strategy_router.post("/subscribe")
async def subscribe_strategy(request: Request):
    try:
        state = await request.json()

        strategy_id = state.get('strategy_id')
        lot = state.get('lot')

        if not strategy_id or not lot:
            return {"status": 400, "message": "Missing 'strategy_id' or 'lot' in the request."}

        bot = bot_manager.create_new_bot(lot)

        strategy = strategy_manager.get_strategy_by_id(strategy_id)

        strategy.subscribe(bot)

        return {"status": 200, "message": "subscribe successfully"}
    except Exception as e:
        return {"status": 500, "message": str(e)}

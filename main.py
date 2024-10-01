from fastapi import FastAPI, WebSocket
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from bot import Bot
from asyncio import sleep
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect
from ws.web_socket import websocket_manager
from ws import ws
import uvicorn
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or specify a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(ws.router)

scheduler = AsyncIOScheduler()
account_id = 176471571  # Your account number
password = os.getenv("password")  # Your MetaTrader password
server = "Exness-MT5Trial7"  # The server for your account
bot = Bot(account_id, password, server, scheduler)


@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass


@app.websocket('/bots/live')
async def bot_live(websocket: WebSocket):
    print("connecting websocket")
    await websocket_manager.connect(websocket)
    try:
        uptime = 0
        while True:
            await sleep(1)
            await websocket_manager.broadcast(str(uptime))
            uptime += 1
    except WebSocketDisconnect as e:
        websocket_manager.disconnect(websocket)
        print("disconnecting websocket: ", e)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

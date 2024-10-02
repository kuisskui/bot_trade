from fastapi import WebSocket
from typing import List


class WebSocketManager:
    def __init__(self):
        self.active_websockets: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_websockets.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_websockets.remove(websocket)
        await websocket.close()

    async def broadcast(self, message: str):
        print(self.active_websockets)
        for websocket in self.active_websockets:
            await websocket.send_text(message)


websocket_manager = WebSocketManager()

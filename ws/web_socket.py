from fastapi import WebSocket
from typing import List


class WebSocketManager:
    def __init__(self):
        self.active_websockets: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_websockets.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_websockets.remove(websocket)

    async def broadcast(self, message: str):
        for websocket in self.active_websockets:
            try:
                await websocket.send_text(message)
            except Exception as e:
                print("WebSocketManager Exception: ", e)


websocket_manager = WebSocketManager()

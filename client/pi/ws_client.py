import asyncio
import websockets


class BLEWebSocketClient:
    def __init__(self, uri, on_message_callback):
        self.uri = uri
        self.on_message_callback = on_message_callback

    async def run(self):
        async with websockets.connect(self.uri) as websocket:
            print("[WebSocket] Connected")
            async for message in websocket:
                print(f"[WebSocket] Received: {message}")
                await self.on_message_callback(message)

import asyncio
from ws_client import BLEWebSocketClient
from ble_controller import BLEController

ble_ctrl = BLEController()


async def main():
    async def handle_ws_message(message: str):
        await ble_ctrl.scan_and_send(message)

    ws = BLEWebSocketClient("ws://192.168.3.xx:9080", handle_ws_message)

    try:
        await ws.run()
    except asyncio.CancelledError:
        print("[Main] Cancelled (likely due to shutdown)")
    except KeyboardInterrupt:
        print("[Main] KeyboardInterrupt detected")
    finally:
        print("[Main] Cleanup and exit")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[Main] Program interrupted and exited gracefully.")

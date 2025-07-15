import asyncio
from ws_client import BLEWebSocketClient
from ble_controller import BLEController

ble = BLEController()


async def main():
    await ble.initialize_connections()

    async def on_message(msg):
        asyncio.create_task(ble.send_to_all(msg))

    ws = BLEWebSocketClient("ws://192.168.3.xx:9080", on_message)

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

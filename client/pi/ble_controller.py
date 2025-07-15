import asyncio
from bleak import BleakScanner, BleakClient

TARGET_NAME_PREFIX = "ESP_LED"
CHARACTERISTIC_UUID = "abcdef01-1234-5678-1234-56789abcdef0"


class BLEController:
    def __init__(self):
        self.clients = {}

    async def initialize_connections(self):
        print("[BLE] Scanning for devices to connect...")
        devices = await BleakScanner.discover(timeout=5.0)

        for d in devices:
            if d.name and d.name.startswith(TARGET_NAME_PREFIX):
                if d.name in self.clients:
                    continue

                print(f"[BLE] Connecting to {d.name} ({d.address})")
                client = BleakClient(d.address)
                try:
                    await client.connect()
                    if client.is_connected:
                        self.clients[d.name] = client
                        print(f"[BLE] Connected to {d.name}")
                    else:
                        print(f"[BLE] Failed to connect to {d.name}")
                except Exception as e:
                    print(f"[BLE] Connection error with {d.name}: {e}")

    async def send_to_all(self, data: str):
        print(f"[BLE] Sending to all: {data}")
        for name, client in self.clients.items():
            if client.is_connected:
                try:
                    await client.write_gatt_char(CHARACTERISTIC_UUID, data.encode())
                    print(f"[BLE] Sent to {name}")
                except Exception as e:
                    print(f"[BLE] Write failed to {name}: {e}")
            else:
                print(f"[BLE] Skipped {name} (not connected)")

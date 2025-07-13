import asyncio
from bleak import BleakScanner, BleakClient

TARGET_NAME_PREFIX = "ESP_LED"
CHARACTERISTIC_UUID = "abcdef01-1234-5678-1234-56789abcdef0"


class BLEController:
    def __init__(self):
        self.target_name = None
        self.target_address = None
        self.connected_client = None

    async def scan_and_send(self, data: str):
        if self.connected_client and self.connected_client.is_connected:
            await self._send_data(data)
            return

        print(f"[BLE] Scanning for device to send: {data}")
        devices = await BleakScanner.discover(timeout=3.0)

        for d in devices:
            if d.name and d.name.startswith(TARGET_NAME_PREFIX):
                print(f"[BLE] Found target: {d.name} ({d.address})")
                self.target_name = d.name
                self.target_address = d.address
                self.connected_client = BleakClient(d.address)
                try:
                    await self.connected_client.connect()
                    print(f"[BLE] Connected to {d.address}")
                    await self._send_data(data)
                except Exception as e:
                    print(f"[BLE] Connection failed: {e}")
                    self.connected_client = None
                return

        print("[BLE] Target device not found")

    async def _send_data(self, data: str):
        try:
            await self.connected_client.write_gatt_char(CHARACTERISTIC_UUID, data.encode())
            print(f"[BLE] Sent: {data}")
        except Exception as e:
            print(f"[BLE] Write error: {e}")
            await self.connected_client.disconnect()
            self.connected_client = None

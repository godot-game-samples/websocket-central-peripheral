import asyncio
from bleak import BleakScanner, BleakClient

TARGET_NAME_PREFIX = "ESP_LED"
CHARACTERISTIC_UUID = "abcdef01-1234-5678-1234-56789abcdef0"


class BLEController:
    def __init__(self):
        self.device_cache = {}

    async def scan_and_send(self, data: str):
        if self.device_cache:
            for addr in self.device_cache.values():
                await self._send_data(addr, data)
            return

        print(f"[BLE] Scanning for devices to send: {data}")
        devices = await BleakScanner.discover(timeout=3.0)

        for d in devices:
            if d.name and d.name.startswith(TARGET_NAME_PREFIX):
                print(f"[BLE] Found: {d.name} ({d.address})")
                self.device_cache[d.name] = d.address
                await self._send_data(d.address, data)

    async def _send_data(self, address: str, data: str):
        try:
            async with BleakClient(address) as client:
                if client.is_connected:
                    print(f"[BLE] Connected to {address}, sending: {data}")
                    await client.write_gatt_char(CHARACTERISTIC_UUID, data.encode())
                    print(f"[BLE] Wrote to {address}")
        except Exception as e:
            print(f"[BLE] Error communicating with {address}: {e}")

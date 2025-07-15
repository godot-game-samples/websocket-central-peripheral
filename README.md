## Websocket Central & Peripheral

<img width="350" src="https://github.com/godot-game-samples/websocket-ble-advertiser/blob/main/assets/screenshot/screen_1.png">

<img width="350" src="https://github.com/godot-game-samples/websocket-ble-advertiser/blob/main/assets/screenshot/screen_2.png">

- Raspberry Pi: Central
- ESP32: Peripheral

### Cached Single connections

I am trying to make multiple connections and the response is slow. For immediacy, [click here.](https://github.com/godot-game-samples/websocket-central-peripheral/tree/feature/single_connection)

### Cached Multiple connections

Here is a form that supports multiple connections, cached and reacts immediately, [click here.](https://github.com/godot-game-samples/websocket-central-peripheral/tree/feature/multi_connection)

```
python3 client/pi/main.py
```

```
[WebSocket] Connected
[WebSocket] Received: LED_ON
[BLE] Scanning for devices to send: LED_ON
[BLE] Found: ESP_LED_1 (CC:DB:A7:98:54:FA)
[BLE] Connected to CC:DB:A7:98:54:FA, sending: LED_ON
[BLE] Wrote to CC:DB:A7:98:54:FA
[WebSocket] Received: LED_OFF
[BLE] Connected to CC:DB:A7:98:54:FA, sending: LED_OFF
[BLE] Wrote to CC:DB:A7:98:54:FA
[WebSocket] Received: LED_ON
```


#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define SERVICE_UUID        "12345678-1234-5678-1234-56789abcdef0"
#define CHARACTERISTIC_UUID "abcdef01-1234-5678-1234-56789abcdef0"
#define DEVICE_NAME         "ESP_LED_1"

#define LED_PIN 2

bool ledState = false;

class MyCharacteristicCallbacks : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic* pCharacteristic) override {
    String value = String(pCharacteristic->getValue().c_str());
    Serial.print("[ESP32] Received via GATT: ");
    Serial.println(value);

    if (value == "LED_ON") {
      digitalWrite(LED_PIN, HIGH);
      ledState = true;
      Serial.println("[LED] Turned ON");
    } else if (value == "LED_OFF") {
      digitalWrite(LED_PIN, LOW);
      ledState = false;
      Serial.println("[LED] Turned OFF");
    } else {
      Serial.println("[ESP32] Unknown command");
    }
  }
};

class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) override {
    Serial.println("[ESP32] Central connected");
  }

  void onDisconnect(BLEServer* pServer) override {
    Serial.println("[ESP32] Central disconnected");
    BLEDevice::startAdvertising(); 
  }
};

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("[ESP32] Starting BLE Peripheral");
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  BLEDevice::init(DEVICE_NAME);
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  BLEService *pService = pServer->createService(SERVICE_UUID);

  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_WRITE
  );
  pCharacteristic->setCallbacks(new MyCharacteristicCallbacks());

  pService->start();

  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();

  Serial.println("[ESP32] Advertising started");
}

void loop() {
  delay(10);
}

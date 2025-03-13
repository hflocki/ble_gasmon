# Home Assistant Custom Integration: BLE Gas Monitor
# Repository: https://github.com/hflocki/ble_gasmon/

import asyncio
import logging
from bleak import BleakClient
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ble_gasmon"
SENSOR_MAC = "90:3E:AB:4D:45:10"  # MAC-Adresse des Sensors
SERVICE_UUID = "0000xxxx-0000-1000-8000-00805f9b34fb"  # Muss noch ermittelt werden
CHARACTERISTIC_UUID = "0000xxxx-0000-1000-8000-00805f9b34fb"  # Muss noch ermittelt werden
PASSKEY = 6484

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    async_add_entities([BleGasMonSensor(entry.data["mac_address"], entry.data["passkey"])]))

class BleGasMonSensor(SensorEntity):
    def __init__(self, mac_address: str, passkey: int):
        self._state = None
        self._mac_address = mac_address
        self._passkey = passkey
        self._name = "BLE Gas Monitor"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        try:
            _LOGGER.info("Verbindet mit BLE-Sensor %s ...", self._mac_address)
            async with BleakClient(self._mac_address) as client:
                await client.pair(self._passkey)  # PIN-Code senden
                data = await client.read_gatt_char(CHARACTERISTIC_UUID)
                self._state = int.from_bytes(data, byteorder='little')
                _LOGGER.info("Füllstand: %s%%", self._state)
        except Exception as e:
            _LOGGER.error("Fehler beim Abrufen der Daten: %s", e)

# Manifest-Datei für Home Assistant
manifest = {
    "domain": DOMAIN,
    "name": "BLE Gas Monitor",
    "version": "1.0.0",
    "requirements": ["bleak"],
    "dependencies": [],
    "codeowners": ["@hflocki"],
    "iot_class": "local_polling"
}

# Konfigurationsdatei für die UI-Einrichtung
config_flow = {
    "type": "form",
    "fields": {
        "mac_address": {"type": "string", "default": SENSOR_MAC},
        "passkey": {"type": "integer", "default": PASSKEY}
    }
}

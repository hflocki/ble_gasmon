DOMAIN = "ble_gasmon"

async def async_setup_entry(hass, entry):
    hass.data.setdefault(DOMAIN, {})
    return True

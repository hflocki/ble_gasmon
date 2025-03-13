from homeassistant import config_entries
from .const import DOMAIN

class BleGasMonConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=vol.Schema({
                vol.Required("mac_address"): str,
                vol.Required("passkey", default=6484): int,
            }))
        return self.async_create_entry(title="BLE Gas Monitor", data=user_input)

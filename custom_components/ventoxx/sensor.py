import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# A clean dictionary mapping the raw fstate to human-readable labels
STATE_MAP = {
    0: "Off",
    17: "HRV Speed 1 - Intake",
    25: "HRV Speed 1 - Exhaust",
    18: "HRV Speed 2 - Intake",
    26: "HRV Speed 2 - Exhaust",
    19: "HRV Speed 3 - Intake",
    27: "HRV Speed 3 - Exhaust",
    1: "Speed 1 - Intake",
    9: "Speed 1 - Exhaust",
    2: "Speed 2 - Intake",
    10: "Speed 2 - Exhaust",
    3: "Speed 3 - Intake",
    11: "Speed 3 - Exhaust",
    6: "Boost Intake",
    14: "Boost Exhaust"
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Ventoxx sensor platform from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([VentoxxModeSensor(coordinator)])

class VentoxxModeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Ventoxx Mode Sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        # Name it automatically based on the device name (e.g., "Kitchen Mode")
        base_name = coordinator.config_entry.data.get("name", "Ventoxx")
        self._attr_name = f"{base_name} Mode"
        
        # Create a unique ID so users can rename it in the UI if they want
        host = coordinator.config_entry.data.get("host", "unknown_host")
        self._attr_unique_id = f"{host}_mode_sensor"

    @property
    def _fstate(self) -> int:
        """Helper to get current fstate from coordinator data."""
        return int(self.coordinator.data.get("fstate", 0))

    @property
    def native_value(self) -> str:
        """Return the state of the sensor (The text label)."""
        f = self._fstate
        return STATE_MAP.get(f, f"Unknown State ({f})")

    @property
    def icon(self) -> str:
        """Return the dynamic icon based on airflow direction."""
        f = self._fstate
        if f == 0:
            return "mdi:fan-off"
        elif f in [6, 14]:
            return "mdi:fan-plus"
        elif f in [1, 2, 3, 17, 18, 19]:
            return "mdi:arrow-down-circle"
        elif f in [9, 10, 11, 25, 26, 27]:
            return "mdi:arrow-up-circle"
        else:
            return "mdi:fan-alert"
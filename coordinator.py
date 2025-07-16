"""DataUpdateCoordinator for our integration."""

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
)
from homeassistant.core import DOMAIN, HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .xlink_ptp import PTPFields
from .hub import Hub
from .const import DEFAULT_SCAN_INTERVAL, DeviceEntity


_LOGGER = logging.getLogger(__name__)


class MyCoordinator(DataUpdateCoordinator):
    """My coordinator."""

    data: list[DeviceEntity]

    def __init__(
        self, hass: HomeAssistant, config_entry: ConfigEntry, hub: Hub
    ) -> None:
        """Initialize coordinator."""

        self.hub = hub
        self.poll_interval = config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )
        self.home_id = config_entry.data[PTPFields.HOME_ID]

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} ({config_entry.unique_id})",
            update_method=self.async_update_data,
            update_interval=timedelta(seconds=self.poll_interval),
        )

    async def async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to retrieve and pre-process the data into an appropriate data structure
        to be used to provide values for all your entities.
        """

        if not self.data:
            self.data = await self.hub.async_get_all_device(self.home_id)
        devices = {}
        for entity in self.data:
            device_id = entity.device_id
            devices[device_id] = entity.product_id
        try:
            raw_devices = await self.hub.async_get_all_device_states(devices)
            if raw_devices:
                for did, device_state in raw_devices.items():
                    for entity in self.data:
                        device_id = entity.device_id
                        if isinstance(device_id, int):
                            device_id = str(device_id)
                        if did == device_id:
                            properies = device_state["properties"]
                            entity.properties.update(properies)
                            entity.raw_data = device_state["raw_data"]
            else:
                _LOGGER.warning("Failed to request device state, result is None")
        except Exception as err:
            raise UpdateFailed(f"Failed to request device state: {err}") from err
        else:
            return self.data

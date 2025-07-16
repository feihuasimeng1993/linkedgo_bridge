"""A demonstration 'hub' that connects several devices."""

from __future__ import annotations

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.
# This dummy hub always returns 3 rollers.
import asyncio
import random
from typing import Any
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    UnitOfTemperature,
)
from .xlink_ptp import PTP
from .const import DeviceEntity


class Hub:
    """Hub for thermostat."""

    manufacturer = "Linkedgo"

    def __init__(self, hass: HomeAssistant, ptp: PTP) -> None:
        """Init dummy hub."""
        self._hass = hass
        self._callbacks = set()
        self.online = True
        self.ptp = ptp

    async def async_get_all_device(self, home_id) -> list[DeviceEntity]:
        """Fetch and normalize state for all supported devices."""
        return await self.ptp.async_home_device(home_id)

    async def async_get_all_device_states(self, devices: dict) -> list[dict[str, Any]]:
        """Fetch and normalize state for all supported devices."""
        return await self.ptp.async_batch_device_state(devices)

    async def async_get_device_states(self, pid: str, did: str) -> dict[str, Any]:
        devices = {}
        did = did if isinstance(did, str) else str(did)
        devices[did] = pid
        raw_devices = await self.ptp.async_batch_device_state(devices)
        if did in raw_devices:
            return raw_devices[did]["properties"]
        return None

    async def async_device_control(
        self, entity: DeviceEntity, property: str, value: Any
    ) -> bool:
        """Set device property."""
        return await self.ptp.async_device_control(entity, property, value)

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Roller changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    # In a real implementation, this library would call it's call backs when it was
    # notified of any state changeds for the relevant device.
    async def publish_updates(self) -> None:
        """Schedule call all registered callbacks."""
        pass
        for callback in self._callbacks:
            callback()

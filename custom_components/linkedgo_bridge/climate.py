"""Platform for sensor integration."""

from __future__ import annotations

from typing import Any
import logging
import asyncio
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.exceptions import HomeAssistantError

# These constants are relevant to the type of entity we are using.
from homeassistant.components.climate import (
    ClimateEntityFeature,
    ClimateEntity,
    ATTR_CURRENT_HUMIDITY,
    ATTR_CURRENT_TEMPERATURE,
    ATTR_FAN_MODES,
    ATTR_FAN_MODE,
    ATTR_PRESET_MODE,
    ATTR_PRESET_MODES,
    ATTR_HUMIDITY,
    ATTR_MAX_HUMIDITY,
    ATTR_MIN_HUMIDITY,
    ATTR_MAX_TEMP,
    ATTR_MIN_TEMP,
    ATTR_HVAC_ACTION,
    ATTR_HVAC_MODES,
    ATTR_HVAC_MODE,
    ATTR_SWING_MODES,
    ATTR_SWING_MODE,
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
    ATTR_TARGET_TEMP_STEP,
    HVACAction,
    HVACMode,
    SERVICE_SET_FAN_MODE,
    SERVICE_SET_PRESET_MODE,
    SERVICE_SET_HUMIDITY,
    SERVICE_SET_HVAC_MODE,
    SERVICE_SET_SWING_MODE,
    SERVICE_SET_TEMPERATURE,
    DOMAIN,
)
from homeassistant.const import UnitOfTemperature, PRECISION_TENTHS, ATTR_TEMPERATURE
from homeassistant.helpers.device_registry import format_mac

from . import MyConfigEntry
from .coordinator import MyCoordinator
from .hub import Hub
from .const import DeviceEntity


logger = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: MyConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add cover for passed config_entry in HA."""
    coordinator = config_entry.runtime_data.coordinator
    devices: list[MyThermostat] = []
    for entity in coordinator.data:
        device_type = entity.ha_type
        if device_type and device_type == DOMAIN:
            devices.append(MyThermostat(coordinator, coordinator.hub, entity))
    async_add_entities(devices)


class MyThermostat(CoordinatorEntity, ClimateEntity):
    """Representation of a dummy Cover."""

    should_poll = False

    supported_features = None

    def __init__(
        self, coordinator: MyCoordinator, hub: Hub, entity: DeviceEntity
    ) -> None:
        super().__init__(coordinator)
        self.hub = hub
        self.entity = entity

        self.supported_features = self.entity.ha_supported_features
        formatted_mac = format_mac(self.entity.device_mac)
        self._attr_unique_id = formatted_mac  # stable ID
        self._attr_name = self.entity.device_name  # shown in UI

        self._attr_fan_mode = self.entity.properties.get(ATTR_FAN_MODE)
        self._attr_hvac_action = self.entity.properties.get(ATTR_HVAC_ACTION)
        self._attr_hvac_mode = self.entity.properties.get(ATTR_HVAC_MODE)
        self._attr_preset_mode = self.entity.properties.get(ATTR_PRESET_MODE)
        self._attr_target_temperature = self.entity.properties.get(
            SERVICE_SET_TEMPERATURE
        )
        self._attr_target_humidity = self.entity.properties.get(SERVICE_SET_HUMIDITY)

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self.entity.device_id)},
            # If desired, the name for the device could be different to the entity
            "name": self.entity.device_name,
            "sw_version": self.entity.sw_version,
            "model": self.entity.product_model,
            "manufacturer": self.hub.manufacturer,
        }

    @property
    def available(self) -> bool:
        return self.hub.online and self.entity.online

    @property
    def current_humidity(self) -> float | None:
        return self.entity.properties[ATTR_CURRENT_HUMIDITY]

    @property
    def current_temperature(self) -> float | None:
        return self.entity.properties[ATTR_CURRENT_TEMPERATURE]

    @property
    def fan_mode(self) -> str | None:
        return self.entity.properties[ATTR_FAN_MODE]

    @property
    def fan_modes(self) -> list[str] | None:
        return self.entity.properties[ATTR_FAN_MODES]

    @property
    def hvac_action(self) -> HVACAction | None:
        return self.entity.properties[ATTR_HVAC_ACTION]

    @property
    def hvac_mode(self) -> HVACMode | None:
        return self.entity.properties[ATTR_HVAC_MODE]

    @property
    def hvac_modes(self) -> list[HVACMode] | None:
        return self.entity.properties[ATTR_HVAC_MODES]

    @property
    def max_humidity(self) -> float | None:
        return self.entity.properties[ATTR_MAX_HUMIDITY]

    @property
    def max_temp(self) -> float | None:
        return self.entity.properties[ATTR_MAX_TEMP]

    @property
    def min_humidity(self) -> float | None:
        return self.entity.properties[ATTR_MIN_HUMIDITY]

    @property
    def min_temp(self) -> float | None:
        return self.entity.properties[ATTR_MIN_TEMP]

    @property
    def precision(self) -> float | None:
        return PRECISION_TENTHS

    @property
    def preset_mode(self) -> str | None:
        return self.entity.properties[ATTR_PRESET_MODE]

    @property
    def preset_modes(self) -> list[str] | None:
        return self.entity.properties[ATTR_PRESET_MODES]

    @property
    def target_humidity(self) -> float | None:
        return self.entity.properties[SERVICE_SET_HUMIDITY]

    @property
    def target_temperature(self) -> float | None:
        return self.entity.properties[SERVICE_SET_TEMPERATURE]

    @property
    def target_temperature_high(self) -> float | None:
        return self.entity.properties[ATTR_TARGET_TEMP_HIGH]

    @property
    def target_temperature_low(self) -> float | None:
        return self.entity.properties[ATTR_TARGET_TEMP_LOW]

    @property
    def target_temperature_step(self) -> float | None:
        return self.entity.properties[ATTR_TARGET_TEMP_STEP]

    @property
    def temperature_unit(self) -> str | None:
        return UnitOfTemperature.CELSIUS

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        ret = await self.hub.async_device_control(
            self.entity,
            SERVICE_SET_HVAC_MODE,
            hvac_mode,
        )
        await self.async_update_state(ret)

    async def async_turn_on(self):
        """Turn the entity on."""
        ret = await self.hub.async_device_control(
            self.entity,
            SERVICE_SET_HVAC_MODE,
            HVACMode.AUTO,
        )
        await self.async_update_state(ret)

    async def async_turn_off(self):
        """Turn the entity off."""
        ret = await self.hub.async_device_control(
            self.entity,
            SERVICE_SET_HVAC_MODE,
            HVACMode.OFF,
        )
        await self.async_update_state(ret)

    async def async_toggle(self):
        """Toggle the entity."""
        pass

    async def async_set_preset_mode(self, preset_mode):
        """Set new target preset mode."""
        ret = await self.hub.async_device_control(
            self.entity,
            SERVICE_SET_PRESET_MODE,
            preset_mode,
        )
        await self.async_update_state(ret)

    async def async_set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        ret = await self.hub.async_device_control(
            self.entity,
            SERVICE_SET_FAN_MODE,
            fan_mode,
        )
        await self.async_update_state(ret)

    async def async_set_humidity(self, humidity):
        """Set new target humidity."""
        ret = await self.hub.async_device_control(
            self.entity,
            SERVICE_SET_HUMIDITY,
            humidity,
        )
        await self.async_update_state(ret)

    # Specific Parameter(**kwargs) when invoke async_set_temperature()
    async def async_set_temperature(self, **kwargs: Any):
        """Set new target temperature."""
        ret = await self.hub.async_device_control(
            self.entity,
            SERVICE_SET_TEMPERATURE,
            kwargs[ATTR_TEMPERATURE],
        )
        await self.async_update_state(ret)

    async def async_update_state(self, opt_ret: bool):
        """Update current device state and UI state."""

        if opt_ret:
            await asyncio.sleep(3)
            states = await self.hub.async_get_device_states(
                self.entity.product_id, self.entity.device_id
            )
            if states:
                self.entity.properties.update(states)
                self.async_write_ha_state()
            else:
                raise HomeAssistantError(
                    f"Failed to request device state {self.entity.device_name}"
                )
        else:
            raise HomeAssistantError(
                f"Failed to control device {self.entity.device_name}"
            )

from typing import Any

from homeassistant.components.climate import (
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
    FAN_ON,
    FAN_OFF,
    FAN_AUTO,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    FAN_TOP,
    FAN_MIDDLE,
    FAN_FOCUS,
    FAN_DIFFUSE,
    SWING_ON,
    SWING_OFF,
    SWING_BOTH,
    SWING_VERTICAL,
    SWING_HORIZONTAL,
    PRESET_NONE,
    PRESET_ECO,
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_COMFORT,
    PRESET_HOME,
    PRESET_SLEEP,
    PRESET_ACTIVITY,
    SERVICE_SET_FAN_MODE,
    SERVICE_SET_PRESET_MODE,
    SERVICE_SET_HUMIDITY,
    SERVICE_SET_HVAC_MODE,
    SERVICE_SET_SWING_MODE,
    SERVICE_SET_TEMPERATURE,
    HVACAction,
    HVACMode,
    ClimateEntityFeature,
    ClimateEntity,
    DOMAIN as CLIMATE_DOMAIN,
)


class ST830:
    """Physical mode, mode: ST1800-HN, pid: 1603bec1cd5903e91603bec1cd599801."""

    ha_type = CLIMATE_DOMAIN
    ha_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )
    model = "ST1800-HN"
    bran = "linkedgo"
    device_name = "thermostat ST1800-HN"

    def __init__(self) -> None:
        """Initiate ST1800-HN physical model class."""
        pass

    @staticmethod
    def attr_current_humidity(state: dict) -> tuple:
        if "21" in state:
            value = state["21"]
            value = value / 10
            return (True, value)
        return (False, None)

    @staticmethod
    def attr_current_temperature(state: dict) -> tuple:
        if "20" in state:
            value = state["20"]
            value = value / 10
            return (True, value)
        return (False, None)

    @staticmethod
    def attr_hvac_action(state: dict) -> tuple:
        if "0" in state and "23" in state:
            switch = state["0"]
            idle_bit = state["23"]
            if switch == 0:
                return (True, HVACAction.OFF)
            elif switch == 1:
                # bit6: cooling standby; bit7: heating standby.
                if (idle_bit & 0x40) > 0:
                    return (True, HVACAction.IDLE)
                else:
                    return (True, HVACAction.HEATING)
            return (False, None)
        return (False, None)

    @staticmethod
    def attr_hvac_mode(state: dict) -> tuple:
        if "0" in state:
            switch = state["0"]
            if switch == 0:
                return (True, HVACMode.OFF)
            else:
                return (True, HVACMode.HEAT)
        return (False, None)

    @staticmethod
    def attr_hvac_modes(state: dict) -> tuple:
        hvac_modes = [
            HVACMode.OFF,
            HVACMode.HEAT,
        ]
        return (True, hvac_modes)

    @staticmethod
    def attr_max_temp(state: dict) -> tuple:
        return (True, 50)

    @staticmethod
    def attr_min_temp(state: dict) -> tuple:
        return (True, 5)

    @staticmethod
    def attr_target_temperature(state: dict) -> tuple:
        if "1" in state:
            value = state["1"]
            value = value / 10
            return (True, value)
        return (False, None)

    @staticmethod
    def attr_target_temperature_high(state: dict) -> tuple:
        return (True, 50)

    @staticmethod
    def attr_target_temperature_low(state: dict) -> tuple:
        return (True, 5)

    @staticmethod
    def attr_target_temperature_step(state: dict) -> tuple:
        return (True, 0.5)

    @staticmethod
    def service_set_hvac_mode(entity: Any, value: Any) -> tuple:
        enum_v = {
            HVACMode.OFF: [{"index": 0, "value": 0}],
            HVACMode.HEAT: [{"index": 0, "value": 1}],
        }
        if value in enum_v:
            dp = enum_v[value]
            return (True, dp)
        return (False, None)

    @staticmethod
    def service_set_temperature(entity: Any, value: Any) -> tuple:
        if value >= 5 and value <= 50:
            dp = [{"index": 1, "value": (value * 10)}]
            return (True, dp)
        return (False, None)

    attributes = {
        ATTR_CURRENT_HUMIDITY: attr_current_humidity,
        ATTR_CURRENT_TEMPERATURE: attr_current_temperature,
        ATTR_HVAC_ACTION: attr_hvac_action,
        ATTR_HVAC_MODE: attr_hvac_mode,
        ATTR_HVAC_MODES: attr_hvac_modes,
        ATTR_MAX_TEMP: attr_max_temp,
        ATTR_MIN_TEMP: attr_min_temp,
        SERVICE_SET_TEMPERATURE: attr_target_temperature,
        ATTR_TARGET_TEMP_HIGH: attr_target_temperature_high,
        ATTR_TARGET_TEMP_LOW: attr_target_temperature_low,
        ATTR_TARGET_TEMP_STEP: attr_target_temperature_step,
    }

    services = {
        SERVICE_SET_HVAC_MODE: service_set_hvac_mode,
        SERVICE_SET_TEMPERATURE: service_set_temperature,
    }

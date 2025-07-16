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
    """Physical mode, mode: ST830, pid: 160042bed58403e9160042bed5842801."""

    ha_type = CLIMATE_DOMAIN
    ha_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
        | ClimateEntityFeature.TARGET_HUMIDITY
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.PRESET_MODE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )
    model = "ST830"
    bran = "linkedgo"
    device_name = "thermostat ST830"

    def __init__(self) -> None:
        """Initiate ST830 physical model class."""
        pass

    @staticmethod
    def attr_current_humidity(state: dict) -> tuple:
        if "117" in state:
            value = state["117"]
            value = value / 10
            return (True, value)
        return (False, None)

    @staticmethod
    def attr_current_temperature(state: dict) -> tuple:
        if "116" in state:
            value = state["116"]
            value = value / 10
            return (True, value)
        return (False, None)

    @staticmethod
    def attr_fan_mode(state: dict) -> tuple:
        alternating = {
            "0": (True, FAN_AUTO),
            "1": (True, FAN_LOW),
            "2": (True, FAN_MEDIUM),
            "3": (True, FAN_HIGH),
        }
        direct = {
            "0": (True, FAN_AUTO),
            "1": (True, FAN_FOCUS),
            "2": (True, FAN_LOW),
            "3": (True, FAN_MEDIUM),
            "4": (True, FAN_HIGH),
            "5": (True, FAN_TOP),
        }
        default = {
            "1": (True, FAN_LOW),
            "2": (True, FAN_MEDIUM),
            "3": (True, FAN_HIGH),
        }
        enum_v = alternating
        if "2" in state and "6" in state:
            machine_type = state["2"]
            fan_mode = state["6"]
            if isinstance(fan_mode, int):
                fan_mode = str(fan_mode)
            if machine_type in [0, 3, 4, 5, 15, 18]:
                enum_v = alternating
            elif machine_type in [1, 6, 7, 8, 16, 19, 20, 21, 22, 23, 24, 25, 82]:
                enum_v = direct
            elif machine_type == 80:
                enum_v = default
            if fan_mode in enum_v:
                return enum_v[fan_mode]
            return (False, None)
        return (False, None)

    @staticmethod
    def attr_fan_modes(state: dict) -> tuple:
        alternating = [FAN_AUTO, FAN_LOW, FAN_MEDIUM, FAN_HIGH]
        direct = [FAN_AUTO, FAN_FOCUS, FAN_LOW, FAN_MEDIUM, FAN_HIGH, FAN_TOP]
        default = [FAN_LOW, FAN_MEDIUM, FAN_HIGH]

        if "2" in state:
            machine_type = state["2"]
            if machine_type in [0, 3, 4, 5, 15, 18]:
                return (True, alternating)
            elif machine_type in [1, 6, 7, 8, 16, 19, 20, 21, 22, 23, 24, 25, 82]:
                return (True, direct)
            elif machine_type == 80:
                return (True, default)
        return (True, alternating)

    @staticmethod
    def attr_hvac_action(state: dict) -> tuple:
        if "0" in state and "1" in state and "130" in state:
            switch = state["0"]
            mode = state["1"]
            idle_bit = state["130"]
            if switch == 0:
                return (True, HVACAction.OFF)
            elif switch == 1:
                # bit6: cooling standby; bit7: heating standby.
                if (idle_bit & 0xC0) > 0:
                    return (True, HVACAction.IDLE)
                if mode == 0:
                    return (True, HVACAction.COOLING)
                elif mode == 1:
                    return (True, HVACAction.HEATING)

            return (False, None)
        return (False, None)

    @staticmethod
    def attr_hvac_mode(state: dict) -> tuple:
        if "0" in state:
            switch = state["0"]
            if switch == 0:
                return (True, HVACMode.OFF)
        if "3" in state:
            user_mode = state["3"]
            if user_mode == 3:
                return (True, HVACMode.DRY)
            elif user_mode == 7:
                return (True, HVACMode.FAN_ONLY)
        if "1" in state:
            main_mode = state["1"]
            if main_mode == 0:
                return (True, HVACMode.COOL)
            elif main_mode == 1:
                return (True, HVACMode.HEAT)
        return (False, None)

    @staticmethod
    def attr_hvac_modes(state: dict) -> tuple:
        hvac_modes = [
            HVACMode.OFF,
            HVACMode.DRY,
            HVACMode.FAN_ONLY,
            HVACMode.COOL,
            HVACMode.HEAT,
        ]
        return (True, hvac_modes)

    @staticmethod
    def attr_max_humidity(state: dict) -> tuple:
        return (True, 75)

    @staticmethod
    def attr_min_humidity(state: dict) -> tuple:
        return (True, 40)

    @staticmethod
    def attr_max_temp(state: dict) -> tuple:
        return (True, 35)

    @staticmethod
    def attr_min_temp(state: dict) -> tuple:
        return (True, 5)

    @staticmethod
    def attr_preset_mode(state: dict) -> tuple:
        if "4" in state:
            sleep_switch = state["4"]
            if sleep_switch == 1:
                return (True, PRESET_SLEEP)
            else:
                return (True, PRESET_NONE)
        return (False, None)

    @staticmethod
    def attr_preset_modes(state: dict) -> tuple:
        preset_modes = [PRESET_NONE, PRESET_SLEEP]
        return (True, preset_modes)

    @staticmethod
    def attr_target_humidity(state: dict) -> tuple:
        if "8" in state:
            value = state["8"]
            return (True, value)
        return (False, None)

    @staticmethod
    def attr_target_temperature(state: dict) -> tuple:
        if "7" in state:
            value = state["7"]
            value = value / 10
            return (True, value)
        return (False, None)

    @staticmethod
    def attr_target_temperature_high(state: dict) -> tuple:
        return (True, 35)

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
            HVACMode.HEAT: [{"index": 0, "value": 1}, {"index": 1, "value": 1}],
            HVACMode.COOL: [{"index": 0, "value": 1}, {"index": 1, "value": 0}],
            HVACMode.HEAT_COOL: [{"index": 0, "value": 1}],
            HVACMode.DRY: [{"index": 0, "value": 1}, {"index": 3, "value": 3}],
            HVACMode.FAN_ONLY: [{"index": 0, "value": 1}, {"index": 3, "value": 7}],
        }
        if value in enum_v:
            dp = enum_v[value]
            return (True, dp)
        return (False, None)

    @staticmethod
    def service_set_preset_mode(entity: Any, value: Any) -> tuple:
        enum_v = {
            PRESET_NONE: [{"index": 4, "value": 0}],
            PRESET_SLEEP: [{"index": 4, "value": 1}],
        }
        if value in enum_v:
            dp = enum_v[value]
            return (True, dp)
        return (False, None)

    @staticmethod
    def service_set_fan_mode(entity: Any, value: Any) -> tuple:
        alternating = {
            FAN_ON: [{"index": 6, "value": 0}],
            FAN_AUTO: [{"index": 6, "value": 0}],
            FAN_LOW: [{"index": 6, "value": 1}],
            FAN_MEDIUM: [{"index": 6, "value": 2}],
            FAN_HIGH: [{"index": 6, "value": 3}],
        }
        direct = {
            FAN_ON: [{"index": 6, "value": 0}],
            FAN_AUTO: [{"index": 6, "value": 0}],
            FAN_FOCUS: [{"index": 6, "value": 1}],
            FAN_LOW: [{"index": 6, "value": 2}],
            FAN_MEDIUM: [{"index": 6, "value": 3}],
            FAN_HIGH: [{"index": 6, "value": 3}],
            FAN_TOP: [{"index": 6, "value": 2}],
        }
        default = {
            FAN_ON: [{"index": 6, "value": 1}],
            FAN_LOW: [{"index": 6, "value": 1}],
            FAN_MEDIUM: [{"index": 6, "value": 2}],
            FAN_HIGH: [{"index": 6, "value": 3}],
        }
        enum_v = alternating
        state = entity.raw_data
        if "2" in state:
            machine_type = state["2"]
            if machine_type in [0, 3, 4, 5, 15, 18]:
                enum_v = alternating
            elif machine_type in [1, 6, 7, 8, 16, 19, 20, 21, 22, 23, 24, 25, 82]:
                enum_v = direct
            elif machine_type == 80:
                enum_v = default
        if value in enum_v:
            dp = enum_v[value]
            return (True, dp)
        return (False, None)

    @staticmethod
    def service_set_humidity(entity: Any, value: Any) -> tuple:
        if value >= 40 and value <= 75:
            dp = [{"index": 8, "value": value}]
            return (True, dp)
        return (False, None)

    @staticmethod
    def service_set_temperature(entity: Any, value: Any) -> tuple:
        if value >= 5 and value <= 35:
            dp = [{"index": 7, "value": (value * 10)}]
            return (True, dp)
        return (False, None)

    attributes = {
        ATTR_CURRENT_HUMIDITY: attr_current_humidity,
        ATTR_CURRENT_TEMPERATURE: attr_current_temperature,
        ATTR_FAN_MODE: attr_fan_mode,
        ATTR_FAN_MODES: attr_fan_modes,
        ATTR_HVAC_ACTION: attr_hvac_action,
        ATTR_HVAC_MODE: attr_hvac_mode,
        ATTR_HVAC_MODES: attr_hvac_modes,
        ATTR_MAX_HUMIDITY: attr_max_humidity,
        ATTR_MIN_HUMIDITY: attr_min_humidity,
        ATTR_MAX_TEMP: attr_max_temp,
        ATTR_MIN_TEMP: attr_min_temp,
        ATTR_PRESET_MODE: attr_preset_mode,
        ATTR_PRESET_MODES: attr_preset_modes,
        SERVICE_SET_HUMIDITY: attr_target_humidity,
        SERVICE_SET_TEMPERATURE: attr_target_temperature,
        ATTR_TARGET_TEMP_HIGH: attr_target_temperature_high,
        ATTR_TARGET_TEMP_LOW: attr_target_temperature_low,
        ATTR_TARGET_TEMP_STEP: attr_target_temperature_step,
    }

    services = {
        SERVICE_SET_HVAC_MODE: service_set_hvac_mode,
        SERVICE_SET_PRESET_MODE: service_set_preset_mode,
        SERVICE_SET_FAN_MODE: service_set_fan_mode,
        SERVICE_SET_HUMIDITY: service_set_humidity,
        SERVICE_SET_TEMPERATURE: service_set_temperature,
    }

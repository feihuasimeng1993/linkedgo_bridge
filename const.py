"""Constants for the example thermostat integration."""

from enum import StrEnum
from dataclasses import dataclass
from typing import Any

# This is the internal name of the integration, it should also match the directory
# name for the integration.
DOMAIN = "linkedgo_bridge"

DEFAULT_SCAN_INTERVAL = 60


@dataclass
class DeviceEntity:
    product_id: str
    product_model: str
    ha_type: str
    ha_supported_features: int
    device_id: str
    device_mac: str
    device_name: str
    sw_version: str
    online: bool
    properties: list[dict[str, Any]]
    raw_data: list[dict[str, Any]]

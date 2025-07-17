from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import (
    CONF_CHOOSE,
    CONF_DESCRIPTION,
    CONF_HOST,
    CONF_MINIMUM,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_SENSORS,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import selector

from .xlink_ptp import PTP, PTPFields, APIAuthError, APIREQUESTError, APIDATAEMPTYError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


STEP_USER_LOGIN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME, description={"phone number or email": "test"}): str,
        vol.Required(CONF_PASSWORD, description={"password": "1234"}): str,
    }
)


async def validate_login(
    hass: HomeAssistant, api: PTP, data: dict[str, Any]
) -> dict[str, Any]:
    """Validate integrations config flow step 1."""
    try:
        user_id = await hass.async_add_executor_job(
            api.user_auth, data[CONF_USERNAME], data[CONF_PASSWORD]
        )
    except APIAuthError as err:
        raise APIAuthError from err
    except APIDATAEMPTYError as err:
        raise APIDATAEMPTYError from err
    return {"user_id": user_id}


class ExampleConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Example Integration."""

    VERSION = 1
    _title: str

    def __init__(self):
        self.api = PTP()
        self.username = None
        self.password = None
        self.home_id = None
        self.user_id = None
        self.homes = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Step 1: User enters credentials."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_login(self.hass, self.api, user_input)
                self.user_id = info["user_id"]
            except APIAuthError:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            if "base" not in errors:
                self.username = user_input[CONF_USERNAME]
                self.password = user_input[CONF_PASSWORD]
                return await self.async_step_select_home()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_LOGIN_SCHEMA,
            errors=errors,
            last_step=False,
        )

    async def async_step_select_home(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Step 2: Let the user select a home."""
        errors: dict[str, str] = {}

        if not self.homes:
            self.homes = await self.api.async_user_home()

        home_options = {
            home[PTPFields.HOME_ID]: home[PTPFields.HOME_NAME] for home in self.homes
        }

        if user_input is not None:
            selected_home_id = user_input["home_id"]
            selected_home_name = home_options[selected_home_id]
            await self.async_set_unique_id(
                selected_home_id
                if isinstance(selected_home_id, str)
                else str(selected_home_id)
            )
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=selected_home_name,
                data={
                    "username": self.username,
                    "password": self.password,
                    "user_id": self.user_id,
                    "home_id": selected_home_id,
                },
            )

        return self.async_show_form(
            step_id="select_home",
            data_schema=vol.Schema({vol.Required("home_id"): vol.In(home_options)}),
            errors=errors,
        )

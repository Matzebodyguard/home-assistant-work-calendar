from __future__ import annotations

import datetime as dt

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    CONF_CALENDAR,
    CONF_END_TIME,
    CONF_START_TIME,
    CONF_SUMMARY,
    DEFAULT_END_TIME,
    DEFAULT_START_TIME,
    DEFAULT_SUMMARY,
    DOMAIN,
)


def _time_string(value: dt.time) -> str:
    return value.strftime("%H:%M:%S")


class WorkCalendarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_CALENDAR])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input[CONF_SUMMARY], data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_CALENDAR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="calendar")
                ),
                vol.Required(CONF_SUMMARY, default=DEFAULT_SUMMARY): str,
                vol.Required(
                    CONF_START_TIME, default=_time_string(DEFAULT_START_TIME)
                ): selector.TimeSelector(),
                vol.Required(
                    CONF_END_TIME, default=_time_string(DEFAULT_END_TIME)
                ): selector.TimeSelector(),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

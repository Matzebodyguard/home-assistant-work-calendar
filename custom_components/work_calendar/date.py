from __future__ import annotations

from datetime import date

from homeassistant.components.date import DateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DATA_SELECTED_DATES, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    dates = hass.data[DOMAIN][DATA_SELECTED_DATES]
    dates.setdefault(entry.entry_id, date.today())
    async_add_entities([WorkdayDate(hass, entry)])


class WorkdayDate(DateEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "workday"
    _attr_icon = "mdi:calendar-edit"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_workday"
        self._attr_name = "Workday"

    @property
    def native_value(self) -> date:
        return self.hass.data[DOMAIN][DATA_SELECTED_DATES][self.entry.entry_id]

    async def async_set_value(self, value: date) -> None:
        self.hass.data[DOMAIN][DATA_SELECTED_DATES][self.entry.entry_id] = value
        self.async_write_ha_state()

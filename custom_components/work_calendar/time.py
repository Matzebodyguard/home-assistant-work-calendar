from __future__ import annotations
from datetime import time
from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from .const import CONF_END_TIME,CONF_START_TIME,DATA_SELECTED_END_TIMES,DATA_SELECTED_START_TIMES,DOMAIN,config_value

def _parse(v):return v if isinstance(v,time) else time.fromisoformat(v)
async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry,async_add_entities:AddConfigEntryEntitiesCallback)->None:
    hass.data[DOMAIN][DATA_SELECTED_START_TIMES].setdefault(entry.entry_id,_parse(config_value(entry,CONF_START_TIME)))
    hass.data[DOMAIN][DATA_SELECTED_END_TIMES].setdefault(entry.entry_id,_parse(config_value(entry,CONF_END_TIME)))
    async_add_entities([SelectedTime(hass,entry,"start","Arbeitsbeginn für ausgewählten Tag",DATA_SELECTED_START_TIMES,"mdi:clock-start"),SelectedTime(hass,entry,"end","Arbeitsende für ausgewählten Tag",DATA_SELECTED_END_TIMES,"mdi:clock-end")])
class SelectedTime(TimeEntity):
    _attr_has_entity_name=True
    def __init__(self,hass,entry,key,name,store,icon):self.hass=hass;self.entry=entry;self.store=store;self._attr_unique_id=f"{entry.entry_id}_selected_{key}_time";self._attr_name=name;self._attr_icon=icon
    @property
    def native_value(self):return self.hass.data[DOMAIN][self.store][self.entry.entry_id]
    async def async_set_value(self,value:time)->None:self.hass.data[DOMAIN][self.store][self.entry.entry_id]=value;self.async_write_ha_state()

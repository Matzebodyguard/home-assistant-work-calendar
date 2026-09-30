from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util
from .const import DATA_SELECTED_DATES,DOMAIN,PLATFORMS
async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry)->bool:
    hass.data.setdefault(DOMAIN,{})
    dates=hass.data[DOMAIN].setdefault(DATA_SELECTED_DATES,{})
    dates.setdefault(entry.entry_id,dt_util.now().date())
    await hass.config_entries.async_forward_entry_setups(entry,PLATFORMS)
    return True
async def async_unload_entry(hass:HomeAssistant,entry:ConfigEntry)->bool:
    unload_ok=await hass.config_entries.async_unload_platforms(entry,PLATFORMS)
    if unload_ok:hass.data.get(DOMAIN,{}).get(DATA_SELECTED_DATES,{}).pop(entry.entry_id,None)
    return unload_ok

from __future__ import annotations
from datetime import datetime,time
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry,ConfigEntryState
from homeassistant.core import HomeAssistant,ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import dt as dt_util
from .const import CONF_CALENDAR,CONF_END_TIME,CONF_EVENT_TITLE,CONF_START_TIME,DOMAIN,PLATFORMS,config_value
SERVICE_SCHEMA=vol.Schema({vol.Required("config_entry_id"):cv.string,vol.Required("date"):cv.date,vol.Optional("start_time"):cv.time,vol.Optional("end_time"):cv.time})
def _t(v):return v if isinstance(v,time) else time.fromisoformat(v)
async def async_setup(hass:HomeAssistant,config:ConfigType)->bool:
 async def add_workday(call:ServiceCall)->None:
  entry=hass.config_entries.async_get_entry(call.data["config_entry_id"])
  if entry is None or entry.domain!=DOMAIN:raise ServiceValidationError("Work Calendar configuration not found")
  if entry.state is not ConfigEntryState.LOADED:raise ServiceValidationError("Work Calendar configuration is not loaded")
  start_clock=call.data.get("start_time") or _t(config_value(entry,CONF_START_TIME));end_clock=call.data.get("end_time") or _t(config_value(entry,CONF_END_TIME))
  if end_clock<=start_clock:raise ServiceValidationError("Arbeitsende muss nach dem Arbeitsbeginn liegen")
  tz=dt_util.DEFAULT_TIME_ZONE;start=datetime.combine(call.data["date"],start_clock,tzinfo=tz);end=datetime.combine(call.data["date"],end_clock,tzinfo=tz)
  await hass.services.async_call("calendar","create_event",{"summary":config_value(entry,CONF_EVENT_TITLE),"start_date_time":start.isoformat(),"end_date_time":end.isoformat()},target={"entity_id":config_value(entry,CONF_CALENDAR)},blocking=True)
 hass.services.async_register(DOMAIN,"add_workday",add_workday,schema=SERVICE_SCHEMA);return True
async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry)->bool:
 await hass.config_entries.async_forward_entry_setups(entry,PLATFORMS);return True
async def async_unload_entry(hass:HomeAssistant,entry:ConfigEntry)->bool:return await hass.config_entries.async_unload_platforms(entry,PLATFORMS)

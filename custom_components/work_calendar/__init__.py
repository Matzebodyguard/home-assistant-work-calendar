from __future__ import annotations
from datetime import datetime
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry,ConfigEntryState
from homeassistant.core import HomeAssistant,ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import dt as dt_util
from .const import CONF_CALENDAR,CONF_END_TIME,CONF_EVENT_TITLE,CONF_START_TIME,DOMAIN,PLATFORMS,config_value
SERVICE_ADD_WORKDAY="add_workday"
ATTR_CONFIG_ENTRY_ID="config_entry_id"
ATTR_DATE="date"
ATTR_START_TIME="start_time"
ATTR_END_TIME="end_time"
SERVICE_SCHEMA=vol.Schema({vol.Required(ATTR_CONFIG_ENTRY_ID):cv.string,vol.Required(ATTR_DATE):cv.date,vol.Optional(ATTR_START_TIME):cv.time,vol.Optional(ATTR_END_TIME):cv.time})
async def async_setup(hass:HomeAssistant,config:ConfigType)->bool:
 async def add_workday(call:ServiceCall)->None:
  entry=hass.config_entries.async_get_entry(call.data[ATTR_CONFIG_ENTRY_ID])
  if entry is None or entry.domain!=DOMAIN:raise ServiceValidationError("Work Calendar configuration not found")
  if entry.state is not ConfigEntryState.LOADED:raise ServiceValidationError("Work Calendar configuration is not loaded")
  work_date=call.data[ATTR_DATE];start_clock=call.data.get(ATTR_START_TIME) or _parse_time(config_value(entry,CONF_START_TIME));end_clock=call.data.get(ATTR_END_TIME) or _parse_time(config_value(entry,CONF_END_TIME))
  if end_clock<=start_clock:raise ServiceValidationError("Arbeitsende muss nach dem Arbeitsbeginn liegen")
  tz=dt_util.DEFAULT_TIME_ZONE;start=datetime.combine(work_date,start_clock,tzinfo=tz);end=datetime.combine(work_date,end_clock,tzinfo=tz)
  await hass.services.async_call("calendar","create_event",{"summary":config_value(entry,CONF_EVENT_TITLE),"start_date_time":start.isoformat(),"end_date_time":end.isoformat()},target={"entity_id":config_value(entry,CONF_CALENDAR)},blocking=True)
 hass.services.async_register(DOMAIN,SERVICE_ADD_WORKDAY,add_workday,schema=SERVICE_SCHEMA)
 return True
def _parse_time(value):
 from datetime import time
 return value if isinstance(value,time) else time.fromisoformat(value)
async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry)->bool:
 await hass.config_entries.async_forward_entry_setups(entry,PLATFORMS);return True
async def async_unload_entry(hass:HomeAssistant,entry:ConfigEntry)->bool:return await hass.config_entries.async_unload_platforms(entry,PLATFORMS)

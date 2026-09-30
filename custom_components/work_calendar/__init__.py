from __future__ import annotations
from datetime import datetime,time
from pathlib import Path
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.lovelace.resources import ResourceStorageCollection
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry,ConfigEntryState
from homeassistant.core import HomeAssistant,ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import dt as dt_util
from .const import CONF_CALENDAR,CONF_END_TIME,CONF_EVENT_TITLE,CONF_START_TIME,DOMAIN,PLATFORMS,config_value
SERVICE_SCHEMA=vol.Schema({vol.Optional("config_entry_id"):cv.string,vol.Required("date"):cv.date,vol.Optional("start_time"):cv.time,vol.Optional("end_time"):cv.time})
def _t(v):return v if isinstance(v,time) else time.fromisoformat(v)
async def async_setup(hass:HomeAssistant,config:ConfigType)->bool:
 frontend_path=Path(__file__).parent/"frontend"
 await hass.http.async_register_static_paths([StaticPathConfig("/work_calendar/work-calendar-card.js",str(frontend_path/"work-calendar-card.js"),False)])
 lovelace=hass.data.get("lovelace")
 if lovelace is not None:
  resources=lovelace.resources if hasattr(lovelace,"resources") else lovelace.get("resources")
  if isinstance(resources,ResourceStorageCollection):
   await resources.async_get_info()
   base="/work_calendar/work-calendar-card.js"
   url=f"{base}?v=0.5.9"
   existing=next((item for item in resources.async_items() if item.get("url","").startswith(base)),None)
   if existing:
    if existing.get("url")!=url or existing.get("res_type")!="module":await resources.async_update_item(existing["id"],{"res_type":"module","url":url})
   else:await resources.async_create_item({"res_type":"module","url":url})
 async def add_workday(call:ServiceCall)->None:
  entry_id=call.data.get("config_entry_id")
  if entry_id:entry=hass.config_entries.async_get_entry(entry_id)
  else:
   entries=[item for item in hass.config_entries.async_entries(DOMAIN) if item.state is ConfigEntryState.LOADED]
   if len(entries)!=1:raise ServiceValidationError("Bitte eine Work-Calendar-Konfiguration angeben, da nicht genau eine geladen ist")
   entry=entries[0]
  if entry is None or entry.domain!=DOMAIN:raise ServiceValidationError("Work Calendar configuration not found")
  if entry.state is not ConfigEntryState.LOADED:raise ServiceValidationError("Work Calendar configuration is not loaded")
  start_clock=call.data.get("start_time") or _t(config_value(entry,CONF_START_TIME));end_clock=call.data.get("end_time") or _t(config_value(entry,CONF_END_TIME))
  if end_clock<=start_clock:raise ServiceValidationError("Arbeitsende muss nach dem Arbeitsbeginn liegen")
  tz=dt_util.DEFAULT_TIME_ZONE;start=datetime.combine(call.data["date"],start_clock,tzinfo=tz);end=datetime.combine(call.data["date"],end_clock,tzinfo=tz)
  await hass.services.async_call("calendar","create_event",{"summary":config_value(entry,CONF_EVENT_TITLE),"start_date_time":start.isoformat(),"end_date_time":end.isoformat()},target={"entity_id":config_value(entry,CONF_CALENDAR)},blocking=True)
  coordinator=hass.data.get(DOMAIN,{}).get("coordinators",{}).get(entry.entry_id)
  if coordinator is not None:await coordinator.async_request_refresh()
 hass.services.async_register(DOMAIN,"add_workday",add_workday,schema=SERVICE_SCHEMA);return True
async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry)->bool:
 await hass.config_entries.async_forward_entry_setups(entry,PLATFORMS);return True
async def async_unload_entry(hass:HomeAssistant,entry:ConfigEntry)->bool:return await hass.config_entries.async_unload_platforms(entry,PLATFORMS)

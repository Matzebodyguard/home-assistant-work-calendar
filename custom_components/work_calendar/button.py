"""Button platform for Work Calendar."""
from __future__ import annotations
from datetime import date,datetime,time,timedelta
from typing import Any,Callable
from homeassistant.components.button import ButtonEntity
from homeassistant.components.calendar import CalendarEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util
from .const import CONF_CALENDAR,CONF_END_TIME,CONF_EVENT_TITLE,CONF_START_TIME,DATA_SELECTED_DATES,DOMAIN,config_value

def _parse_time(v:str|time)->time: return v if isinstance(v,time) else time.fromisoformat(v)
async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry,async_add_entities:AddConfigEntryEntitiesCallback)->None:
 async_add_entities([WorkCalendarButton(hass,entry,"worked_today","Heute gearbeitet","mdi:briefcase-check",lambda:dt_util.now().date()),WorkCalendarButton(hass,entry,"worked_yesterday","Gestern gearbeitet","mdi:calendar-arrow-left",lambda:dt_util.now().date()-timedelta(days=1)),WorkCalendarButton(hass,entry,"worked_selected","Ausgewählten Tag eintragen","mdi:calendar-check",lambda:hass.data[DOMAIN][DATA_SELECTED_DATES][entry.entry_id])])
class WorkCalendarButton(ButtonEntity):
 _attr_has_entity_name=True
 def __init__(self,hass,entry,key,name,icon,date_resolver): self.hass=hass;self._entry=entry;self._date_resolver=date_resolver;self._attr_unique_id=f"{entry.entry_id}_{key}";self._attr_name=name;self._attr_icon=icon
 @property
 def available(self):
  state=self.hass.states.get(config_value(self._entry,CONF_CALENDAR));return state is not None and bool(int(state.attributes.get("supported_features",0))&CalendarEntityFeature.CREATE_EVENT)
 async def async_press(self):
  work_date=self._date_resolver();cal=config_value(self._entry,CONF_CALENDAR);title=config_value(self._entry,CONF_EVENT_TITLE);tz=dt_util.DEFAULT_TIME_ZONE
  start=datetime.combine(work_date,_parse_time(config_value(self._entry,CONF_START_TIME)),tzinfo=tz);end=datetime.combine(work_date,_parse_time(config_value(self._entry,CONF_END_TIME)),tzinfo=tz);ds=datetime.combine(work_date,time.min,tzinfo=tz);de=ds+timedelta(days=1)
  response:dict[str,Any]|None=await self.hass.services.async_call("calendar","get_events",{"start_date_time":ds.isoformat(),"end_date_time":de.isoformat()},target={"entity_id":cal},blocking=True,return_response=True)
  for e in (response or {}).get(cal,{}).get("events",[]):
   es=dt_util.parse_datetime(str(e.get("start","")));ee=dt_util.parse_datetime(str(e.get("end","")))
   if e.get("summary")==title and es and ee and dt_util.as_local(es)==start and dt_util.as_local(ee)==end:return
  await self.hass.services.async_call("calendar","create_event",{"summary":title,"start_date_time":start.isoformat(),"end_date_time":end.isoformat()},target={"entity_id":cal},blocking=True)

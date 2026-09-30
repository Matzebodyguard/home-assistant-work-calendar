"""Monthly Work Calendar statistics."""
from __future__ import annotations
from typing import Any
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util
from .const import CONF_CALENDAR,CONF_EVENT_TITLE,config_value
async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry,async_add_entities:AddConfigEntryEntitiesCallback)->None:async_add_entities([MonthlyWorkDays(hass,entry),MonthlyWorkHours(hass,entry)],True)
class MonthlyBase(SensorEntity):
 _attr_has_entity_name=True
 def __init__(self,hass,entry,key,name,icon):self.hass=hass;self.entry=entry;self._attr_unique_id=f"{entry.entry_id}_{key}";self._attr_name=name;self._attr_icon=icon;self._attr_native_value=0
 async def _events(self)->list[dict[str,Any]]:
  start=dt_util.now().replace(day=1,hour=0,minute=0,second=0,microsecond=0);end=start.replace(year=start.year+1,month=1) if start.month==12 else start.replace(month=start.month+1);cal=config_value(self.entry,CONF_CALENDAR)
  response=await self.hass.services.async_call("calendar","get_events",{"start_date_time":start.isoformat(),"end_date_time":end.isoformat()},target={"entity_id":cal},blocking=True,return_response=True);title=config_value(self.entry,CONF_EVENT_TITLE)
  return [e for e in (response or {}).get(cal,{}).get("events",[]) if e.get("summary")==title]
class MonthlyWorkDays(MonthlyBase):
 _attr_native_unit_of_measurement="d"
 def __init__(self,hass,entry):super().__init__(hass,entry,"days_this_month","Arbeitstage diesen Monat","mdi:calendar-month")
 async def async_update(self):
  days=set()
  for e in await self._events():
   s=dt_util.parse_datetime(str(e.get("start","")))
   if s:days.add(dt_util.as_local(s).date())
  self._attr_native_value=len(days)
class MonthlyWorkHours(MonthlyBase):
 _attr_native_unit_of_measurement="h";_attr_suggested_display_precision=1
 def __init__(self,hass,entry):super().__init__(hass,entry,"hours_this_month","Arbeitsstunden diesen Monat","mdi:clock-outline")
 async def async_update(self):
  total=0.0
  for e in await self._events():
   s=dt_util.parse_datetime(str(e.get("start","")));en=dt_util.parse_datetime(str(e.get("end","")))
   if s and en:total+=(en-s).total_seconds()/3600
  self._attr_native_value=round(total,2)

"""Monthly Work Calendar day statistics."""
from __future__ import annotations
from datetime import datetime
from typing import Any
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util
from .const import CONF_CALENDAR,CONF_EVENT_TITLE,config_value
async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry,async_add_entities:AddConfigEntryEntitiesCallback)->None:
    async_add_entities([MonthlyWorkDays(hass,entry,0,"days_this_month","Arbeitstage diesen Monat"),MonthlyWorkDays(hass,entry,-1,"days_last_month","Arbeitstage letzten Monat")],True)
class MonthlyWorkDays(SensorEntity):
    _attr_has_entity_name=True
    _attr_native_unit_of_measurement="d"
    _attr_icon="mdi:calendar-month"
    def __init__(self,hass:HomeAssistant,entry:ConfigEntry,offset:int,key:str,name:str):
        self.hass=hass;self.entry=entry;self.offset=offset;self._attr_unique_id=f"{entry.entry_id}_{key}";self._attr_name=name;self._attr_native_value=0
    def _range(self):
        now=dt_util.now();current=now.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        if self.offset==0:start=current
        else:start=current.replace(year=current.year-1,month=12) if current.month==1 else current.replace(month=current.month-1)
        end=start.replace(year=start.year+1,month=1) if start.month==12 else start.replace(month=start.month+1)
        return start,end
    async def async_update(self)->None:
        start,end=self._range();cal=config_value(self.entry,CONF_CALENDAR);title=config_value(self.entry,CONF_EVENT_TITLE)
        response:dict[str,Any]|None=await self.hass.services.async_call("calendar","get_events",{"start_date_time":start.isoformat(),"end_date_time":end.isoformat()},target={"entity_id":cal},blocking=True,return_response=True)
        days=set()
        for event in (response or {}).get(cal,{}).get("events",[]):
            if event.get("summary")!=title:continue
            event_start=dt_util.parse_datetime(str(event.get("start","")))
            if event_start:days.add(dt_util.as_local(event_start).date())
        self._attr_native_value=len(days)

from __future__ import annotations
import datetime as dt
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import CONF_CALENDAR,CONF_END_TIME,CONF_EVENT_TITLE,CONF_START_TIME,DEFAULT_END_TIME,DEFAULT_EVENT_TITLE,DEFAULT_START_TIME,DOMAIN

def _ts(v:dt.time)->str:return v.strftime("%H:%M:%S")
def _schema(values):
 return vol.Schema({vol.Required(CONF_CALENDAR,default=values[CONF_CALENDAR]):selector.EntitySelector(selector.EntitySelectorConfig(domain="calendar")),vol.Required(CONF_EVENT_TITLE,default=values[CONF_EVENT_TITLE]):str,vol.Required(CONF_START_TIME,default=values[CONF_START_TIME]):selector.TimeSelector(),vol.Required(CONF_END_TIME,default=values[CONF_END_TIME]):selector.TimeSelector()})
def _valid(data):return dt.time.fromisoformat(data[CONF_END_TIME])>dt.time.fromisoformat(data[CONF_START_TIME])
class WorkCalendarConfigFlow(config_entries.ConfigFlow,domain=DOMAIN):
 VERSION=1
 @staticmethod
 def async_get_options_flow(config_entry):return WorkCalendarOptionsFlow(config_entry)
 async def async_step_user(self,user_input=None):
  errors={}
  if user_input is not None:
   if not _valid(user_input):errors["base"]="end_before_start"
   else:
    await self.async_set_unique_id(user_input[CONF_CALENDAR]);self._abort_if_unique_id_configured();return self.async_create_entry(title=user_input[CONF_EVENT_TITLE],data=user_input)
  values={CONF_CALENDAR:"calendar.",CONF_EVENT_TITLE:DEFAULT_EVENT_TITLE,CONF_START_TIME:_ts(DEFAULT_START_TIME),CONF_END_TIME:_ts(DEFAULT_END_TIME)}
  return self.async_show_form(step_id="user",data_schema=_schema(values),errors=errors)
class WorkCalendarOptionsFlow(config_entries.OptionsFlow):
 def __init__(self,entry):self.entry=entry
 async def async_step_init(self,user_input=None):
  errors={}
  if user_input is not None:
   if not _valid(user_input):errors["base"]="end_before_start"
   else:return self.async_create_entry(title="",data=user_input)
  values={k:self.entry.options.get(k,self.entry.data[k]) for k in (CONF_CALENDAR,CONF_EVENT_TITLE,CONF_START_TIME,CONF_END_TIME)}
  return self.async_show_form(step_id="init",data_schema=_schema(values),errors=errors)

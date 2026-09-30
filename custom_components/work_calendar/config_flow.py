from __future__ import annotations
import datetime as dt
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import CONF_CALENDAR,CONF_END_TIME,CONF_EVENT_TITLE,CONF_START_TIME,DEFAULT_END_TIME,DEFAULT_EVENT_TITLE,DEFAULT_START_TIME,DOMAIN

def _ts(v:dt.time)->str:return v.strftime("%H:%M:%S")
class WorkCalendarConfigFlow(config_entries.ConfigFlow,domain=DOMAIN):
 VERSION=1
 async def async_step_user(self,user_input=None):
  errors={}
  if user_input is not None:
   if dt.time.fromisoformat(user_input[CONF_END_TIME])<=dt.time.fromisoformat(user_input[CONF_START_TIME]):errors["base"]="end_before_start"
   else:
    await self.async_set_unique_id(user_input[CONF_CALENDAR]);self._abort_if_unique_id_configured();return self.async_create_entry(title=user_input[CONF_EVENT_TITLE],data=user_input)
  schema=vol.Schema({vol.Required(CONF_CALENDAR):selector.EntitySelector(selector.EntitySelectorConfig(domain="calendar")),vol.Required(CONF_EVENT_TITLE,default=DEFAULT_EVENT_TITLE):str,vol.Required(CONF_START_TIME,default=_ts(DEFAULT_START_TIME)):selector.TimeSelector(),vol.Required(CONF_END_TIME,default=_ts(DEFAULT_END_TIME)):selector.TimeSelector()})
  return self.async_show_form(step_id="user",data_schema=schema,errors=errors)

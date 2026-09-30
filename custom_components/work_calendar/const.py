from datetime import time
DOMAIN="work_calendar"
PLATFORMS=["button","sensor"]
CONF_CALENDAR="calendar_entity"
CONF_EVENT_TITLE="event_title"
CONF_START_TIME="start_time"
CONF_END_TIME="end_time"
DEFAULT_EVENT_TITLE="Arbeit"
DEFAULT_START_TIME=time(17,0)
DEFAULT_END_TIME=time(21,0)
DATA_SELECTED_DATES="selected_dates"
DATA_SELECTED_START_TIMES="selected_start_times"
DATA_SELECTED_END_TIMES="selected_end_times"
def config_value(entry,key):return entry.options.get(key,entry.data[key])

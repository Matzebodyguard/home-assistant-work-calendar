from datetime import time

DOMAIN = "work_calendar"
PLATFORMS = ["button", "date"]
CONF_CALENDAR = "calendar_entity"
CONF_SUMMARY = "summary"
CONF_START_TIME = "start_time"
CONF_END_TIME = "end_time"
DEFAULT_SUMMARY = "Arbeit"
DEFAULT_START_TIME = time(17, 0)
DEFAULT_END_TIME = time(21, 0)
DATA_SELECTED_DATES = "selected_dates"

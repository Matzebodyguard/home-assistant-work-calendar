"""Monthly Work Calendar day statistics."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.util import dt as dt_util

from .const import CONF_CALENDAR, CONF_EVENT_TITLE, DOMAIN, config_value


def _month_bounds() -> tuple[datetime, datetime, datetime]:
    now = dt_util.now()
    current = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    previous = (
        current.replace(year=current.year - 1, month=12)
        if current.month == 1
        else current.replace(month=current.month - 1)
    )
    next_month = (
        current.replace(year=current.year + 1, month=1)
        if current.month == 12
        else current.replace(month=current.month + 1)
    )
    return previous, current, next_month


def _event_date(value: Any) -> date | None:
    if not value:
        return None
    text = str(value)
    parsed = dt_util.parse_datetime(text)
    if parsed is not None:
        return dt_util.as_local(parsed).date()
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    async def async_update_data() -> dict[str, int]:
        previous, current, next_month = _month_bounds()
        calendar = config_value(entry, CONF_CALENDAR)
        title = config_value(entry, CONF_EVENT_TITLE)
        try:
            response: dict[str, Any] | None = await hass.services.async_call(
                "calendar",
                "get_events",
                {
                    "start_date_time": previous.isoformat(),
                    "end_date_time": next_month.isoformat(),
                },
                target={"entity_id": calendar},
                blocking=True,
                return_response=True,
            )
        except Exception as err:
            raise UpdateFailed(f"Could not read calendar {calendar}: {err}") from err

        current_days: set[date] = set()
        previous_days: set[date] = set()
        for event in (response or {}).get(calendar, {}).get("events", []):
            if event.get("summary") != title:
                continue
            event_day = _event_date(event.get("start"))
            if event_day is None:
                continue
            if current.date() <= event_day < next_month.date():
                current_days.add(event_day)
            elif previous.date() <= event_day < current.date():
                previous_days.add(event_day)

        return {
            "days_this_month": len(current_days),
            "days_last_month": len(previous_days),
        }

    coordinator = DataUpdateCoordinator(
        hass,
        logger=__import__("logging").getLogger(__name__),
        name=f"{DOMAIN}_{entry.entry_id}_monthly_stats",
        update_method=async_update_data,
        update_interval=timedelta(minutes=5),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {}).setdefault("coordinators", {})[entry.entry_id] = coordinator
    async_add_entities(
        [
            MonthlyWorkDays(coordinator, entry, "days_this_month", "Arbeitstage diesen Monat"),
            MonthlyWorkDays(coordinator, entry, "days_last_month", "Arbeitstage letzten Monat"),
        ]
    )


class MonthlyWorkDays(CoordinatorEntity, SensorEntity):
    """A monthly work-day counter."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = "d"
    _attr_icon = "mdi:calendar-month"

    def __init__(self, coordinator, entry: ConfigEntry, key: str, name: str) -> None:
        super().__init__(coordinator)
        self.entry = entry
        self.key = key
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_name = name

    @property
    def native_value(self) -> int:
        return self.coordinator.data.get(self.key, 0)

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        return {
            "work_calendar_stat": self.key,
            "work_calendar_entry_id": self.entry.entry_id,
        }

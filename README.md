# Work Calendar for Home Assistant

A small custom integration for Home Assistant that makes it easy to record workdays in a calendar with one click.

## Features

- **Worked today** button
- **Worked yesterday** button
- Select a custom date and add it with **Add selected workday**
- Configurable target calendar
- Configurable event title
- Configurable default start and end times
- Defaults to **17:00–21:00**
- Duplicate protection for matching work events
- German and English translations
- UI-based setup (Config Flow)

## Installation

### HACS (custom repository)

1. Open HACS in Home Assistant.
2. Add this repository as a custom repository of type **Integration**.
3. Install **Work Calendar**.
4. Restart Home Assistant.
5. Go to **Settings → Devices & services → Add integration**.
6. Search for **Work Calendar**.

### Manual installation

Copy:

```
custom_components/work_calendar/
```

to:

```
/config/custom_components/work_calendar/
```

Then restart Home Assistant and add **Work Calendar** from **Settings → Devices & services**.

## Configuration

During setup you can select:

- Calendar
- Event title (default: `Arbeit`)
- Start time (default: `17:00`)
- End time (default: `21:00`)

The selected calendar must support creating events.

## Entities

The integration provides:

- **Worked today** — creates today's work event
- **Worked yesterday** — creates yesterday's work event
- **Workday** — date selector for a custom date
- **Add selected workday** — creates an event for the selected date

Before creating an event, Work Calendar checks the selected calendar for an existing matching event.

## Example

With the defaults, pressing **Worked today** creates:

```
Arbeit
17:00–21:00
```

on the current date.

## Requirements

- Home Assistant
- A calendar entity that supports creating events

## License

MIT

## Version 0.3.0

- Added **Workdays this month** sensor.
- Added **Work hours this month** sensor.
- Calendar, event title and default start/end times can now be changed from the integration options.
- Monthly statistics are calculated from matching events in the configured calendar, so direct calendar edits are reflected automatically.

### Editing existing calendar events

Home Assistant currently exposes calendar event update/delete capabilities to its frontend, but not as public `calendar.update_event` / `calendar.delete_event` actions. For that reason Work Calendar does not modify or delete existing events programmatically in v0.3.0. Existing events can be edited in Home Assistant's Calendar dashboard; the monthly sensors will then reflect the changed calendar data.

## Version 0.3.1

### Recording another day

Home Assistant button entities cannot open an input dialog. To record another workday:

1. Set **Anderen Arbeitstag auswählen** to the required date.
2. Press **Ausgewählten Tag eintragen**.

The integration then creates the configured work event (default: 17:00–21:00) on that selected date. The selected date is initialized reliably when the integration loads.

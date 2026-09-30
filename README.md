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

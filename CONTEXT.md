# PlannerOS Context

## Current Status

Version:
v0.4.0

## Current Architecture

```text
Clipboard
↓
Parser
↓
PlannerCommand
↓
Dispatcher
↓
Google Calendar
↓
Markdown Tasks
↓
Obsidian Notes
```

## Current Integrations

- Google Calendar integration via `GoogleCalendarService`
- Obsidian note writing via `ObsidianService`
- Markdown task file writing via `TasksService`
- Shared logging and dispatcher orchestration

## Execution Flow

```text
Clipboard
↓
PlannerPipeline
↓
PlannerParser
↓
PlannerCommand
↓
Dispatcher
├── CalendarHandler
├── TasksHandler
└── ObsidianHandler
```

## Testing Status

- 57 automated tests
- Includes parser, dispatcher, handlers, hotkey, logging, clipboard, pipeline, calendar, Obsidian, tasks, and end-to-end coverage

## Completed Releases

- v0.1.0 — Core MVP
- v0.2.0 — Google Calendar Integration
- v0.3.0 — Obsidian Integration
- v0.4.0 — Markdown Tasks

## Known Limitations

- No duplicate calendar detection
- No event updates
- No recurring events
- Markdown task appending only
- No task synchronization
- No Obsidian templates
- No frontmatter generation

## Current Roadmap

- CAL-004 — Duplicate Calendar Detection
- CAL-005 — Event Updates
- CONFIG-001 — Configuration File
- WIN-001 — Windows Packaging
- v1.0.0 — Stable Release

## Implementation Conventions

- Handler = orchestration only
- Service = external integrations
- Dispatcher never performs business logic
- Parser remains independent
- New integrations should follow the Handler → Service pattern

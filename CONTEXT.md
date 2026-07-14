
# PlannerOS Context

## Current Status

Version:
v0.1.0-alpha.3

## Architecture

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

## Completed

- Parser
- Clipboard
- Pipeline
- Hotkey
- Logging
- Dispatcher
- Calendar Handler
- Tasks Handler
- Obsidian Handler
- End-to-End Test

## Testing

43 passing tests

## Remaining

- README
- GitHub Release
- v0.1.0-beta.1

## Rules

- One responsibility per class.
- No compatibility wrappers.
- Use handler classes directly.
- Parser returns PlannerCommand.
- Dispatcher routes validated PlannerCommand.
- Every feature requires tests.

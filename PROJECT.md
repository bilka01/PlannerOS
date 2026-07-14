# PlannerOS

PlannerOS is a local AI-powered productivity assistant that turns ChatGPT plans into executable actions.

The application itself does not generate plans.

Instead:

- ChatGPT creates the plan.
- PlannerOS validates it.
- PlannerOS executes it.

## Current Status

✅ Core Architecture

✅ Testing

✅ End-to-End Integration

✅ Google Calendar

✅ Obsidian

✅ Markdown Tasks

## Features

- Global hotkey
- Clipboard integration
- Planner block parser
- JSON schema validation
- Command dispatcher
- Modular handlers
- Google Calendar integration
- Obsidian Markdown note writing
- Markdown task file writing

## Installation

1. Clone the repository and move into it:

   ```bash
   git clone <repo-url>
   cd PlannerOS
   ```
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. Install runtime dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Install development dependencies (for running tests):

   ```bash
   pip install -r requirements-dev.txt
   ```
5. Run the test suite to confirm everything is working:

   ```bash
   python -m pytest -q
   ```
6. Start PlannerOS:

   ```bash
   python main.py
   ```

   Copy a ChatGPT response containing a planner block to your clipboard, then press `Ctrl+Shift+P` to import it.

## Architecture

```text
ChatGPT
    │
    ▼
Planner Block
    │
    ▼
Clipboard
    │
    ▼
PlannerPipeline
    │
    ▼
PlannerParser
    │
    ▼
PlannerCommand
    │
    ▼
Dispatcher
    ├── CalendarHandler
    │      ▼
    │   GoogleCalendarService
    │      ▼
    │ Google Calendar
    ├── TasksHandler
    │      ▼
    │    TasksService
    │      ▼
    │ Markdown Tasks
    └── ObsidianHandler
           ▼
      ObsidianService
           ▼
      Markdown Notes
```

## Project Structure

```text
PlannerOS/

app/
    clipboard/
    core/
    exceptions/
    handlers/
    hotkeys/
    integrations/
    models/
    parser/
    utils/

tests/
vault/
logs/
```

## Documentation

- `README.md` — project overview
- `PROJECT.md` — architecture and roadmap
- `AGENTS.md` — AI development guidelines

## Technology

- Python 3.12+
- pytest
- pathlib
- logging
- keyboard
- pyperclip

## Release History

- v0.1.0 — Core MVP
- v0.2.0 — Google Calendar Integration
- v0.3.0 — Obsidian Integration
- v0.4.0 — Markdown Tasks

## Roadmap

- CAL-004 — Duplicate Calendar Detection
- CAL-005 — Event Updates
- CONFIG-001 — Configuration File
- WIN-001 — Windows Packaging
- v1.0.0 — Stable Release

## License

MIT

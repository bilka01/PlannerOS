# PlannerOS

PlannerOS is a local productivity assistant that turns structured planner blocks into validated, typed commands and routes them through a simple execution pipeline.

PlannerOS does not generate plans. ChatGPT creates the planner block, and PlannerOS imports, validates, and dispatches it.

## Features

- Clipboard import for planner blocks copied from ChatGPT
- Planner parsing using explicit start and end markers
- Planner pipeline that coordinates clipboard reading, parsing, and dispatching
- Typed `PlannerCommand` objects used after parsing
- Dispatcher that routes validated commands to handlers
- Calendar handler that logs calendar actions
- Tasks handler that logs task actions
- Obsidian handler that logs note update actions
- Global hotkey listener (`Ctrl+Shift+P`) to trigger imports
- Shared logging across the application
- Automated test coverage, including an end-to-end integration test

## Architecture

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

`Clipboard`
Reads text from the system clipboard.

`PlannerPipeline`
Coordinates the import flow by reading clipboard text, parsing it, and dispatching the resulting command.

`PlannerParser`
Extracts the planner block, parses JSON, validates the payload, and constructs a typed `PlannerCommand`.

`PlannerCommand`
The validated domain object passed through the dispatcher and handlers.

`Dispatcher`
Routes validated command sections to the appropriate handlers.

`CalendarHandler`, `TasksHandler`, `ObsidianHandler`
MVP handlers that receive validated data and log the actions PlannerOS would perform.

## Project Structure

```text
app/
  clipboard/
  core/
  exceptions/
  handlers/
  hotkeys/
  models/
  parser/
  utils/
tests/
logs/
README.md
PROJECT.md
AGENTS.md
main.py
```

## Requirements

- Python 3.12+
- A virtual environment for local development
- Windows is the primary runtime target because PlannerOS uses a global hotkey listener and system clipboard access
- WSL can be useful for development and test workflows, but runtime behavior for hotkeys and clipboard access depends on your host environment

## Installation

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd ai_planner
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install runtime dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Install development dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

## Running

Start PlannerOS with:

```bash
python main.py
```

When the application is running, copy a ChatGPT response that contains a planner block and press `Ctrl+Shift+P` to trigger the import pipeline.

## Running Tests

Run the test suite with:

```bash
pytest
```

The project currently contains 43 automated tests, including parser, dispatcher, handler, hotkey, logging, clipboard, pipeline, and end-to-end coverage.

## Current Status

PlannerOS is MVP feature complete for `v0.1.0-beta.1`.

The current handlers are intentionally log-only. They receive validated command data and log what would be executed, but they do not yet perform live integrations with Google Calendar, task systems, or Obsidian files.

## Roadmap

Planned future work includes:

- Google Calendar integration
- Real Obsidian file writing
- Task integrations
- Notifications
- Desktop UI

## Contributing

Contributions are welcome. Please keep changes focused, follow the existing architecture, add or update tests when practical, and run `pytest` before submitting a pull request.

## License

MIT

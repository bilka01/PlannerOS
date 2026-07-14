# PlannerOS

PlannerOS is an AI-powered productivity automation tool that processes structured planner blocks and performs actions across multiple productivity applications.

PlannerOS does not generate plans. ChatGPT creates the planner block, and PlannerOS imports, validates, and dispatches it.

## Current Features

- ✅ Clipboard monitoring
- ✅ Global hotkey
- ✅ Planner block parser
- ✅ JSON schema validation
- ✅ Planner pipeline
- ✅ Dispatcher
- ✅ Google Calendar integration
- ✅ Obsidian integration
- ✅ Markdown task writing
- ✅ Comprehensive automated tests

## Architecture

```text
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
        │        ▼
        │   GoogleCalendarService
        │        ▼
        │ Google Calendar
        │
        ├── TasksHandler
        │        ▼
        │    TasksService
        │        ▼
        │   Markdown Tasks
        │
        └── ObsidianHandler
                 ▼
          ObsidianService
                 ▼
          Markdown Notes
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
Handlers that orchestrate integration-specific services for calendar events, markdown tasks, and markdown notes.

## Project Structure

```text
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
6. Configure Google OAuth credentials and the environment variables below.

### Environment Variables

- `PLANNEROS_GOOGLE_CLIENT_SECRET_FILE` — path to the Google OAuth client secret JSON file
- `PLANNEROS_GOOGLE_TOKEN_FILE` — path to the Google OAuth token file
- `PLANNEROS_OBSIDIAN_VAULT` — path to the Obsidian vault directory
- `PLANNEROS_TASKS_FILE` — path to the markdown task file

## Usage

1. Run PlannerOS:

   ```bash
   python main.py
   ```
2. Copy a planner block containing calendar, tasks, or Obsidian instructions into the clipboard.
3. Press `Ctrl+Shift+P` to trigger the import pipeline.
4. PlannerOS processes the planner block and writes output to:
   - Google Calendar
   - Markdown tasks file
   - Obsidian notes

## Running Tests

Run the test suite with:

```bash
python -m pytest -q
```

The project currently contains 57 automated tests covering parser, dispatcher, handler, hotkey, logging, clipboard, pipeline, calendar, Obsidian, tasks, and end-to-end flows.

## Current Limitations

- No duplicate calendar detection
- No event updates
- No recurring events
- Markdown task appending only
- No task synchronization
- No Obsidian templates
- No frontmatter generation

## Contributing

Contributions are welcome. Please keep changes focused, follow the existing architecture, add or update tests when practical, and run `pytest` before submitting a pull request.

## License

MIT

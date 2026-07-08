
# PlannerOS

PlannerOS is a local AI-powered productivity assistant that turns ChatGPT plans into executable actions.

The application itself does not generate plans.

Instead:

- ChatGPT creates the plan.
- PlannerOS validates it.
- PlannerOS executes it.

## Features (MVP)

- Global hotkey
- Clipboard integration
- Planner block parser
- JSON validation
- Command dispatcher
- Modular handlers

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
   pytest
   ```
6. Start PlannerOS:

   ```bash
   python main.py
   ```

   Copy a ChatGPT response containing a planner block to your clipboard, then press `Ctrl+Shift+P` to import it.

## Architecture

```
ChatGPT
    │
    ▼
Planner Block
    │
    ▼
Clipboard
    │
    ▼
Parser
    │
    ▼
PlannerCommand
    │
    ▼
Dispatcher
    │
    ├── Calendar
    ├── Tasks
    └── Obsidian
```

## Current Status

🚧 MVP v0.1 in development

Current focus:

- Parser
- Dispatcher
- Clipboard
- Hotkey
- Logging

No external integrations are implemented yet.

## Project Structure

```
PlannerOS/

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

## Roadmap

- MVP execution flow
- Google Calendar
- Obsidian
- Statistics
- Analytics
- Local AI support

## License

TBD

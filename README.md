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
# PlannerOS

Short description

---

## Features

- Clipboard import
- Planner parser
- Global hotkey
- Calendar handler
- Tasks handler
- Obsidian handler

---

## Architecture

Diagram

---

## Requirements

Python

WSL

Virtual environment

---

## Installation

git clone

python -m venv

pip install

---

## Running

python main.py

---

## Running Tests

pytest

---

## Project Structure

app/

tests/

logs/

...

---

## Development Workflow

Issue

↓

Implement

↓

pytest

↓

Commit

↓

Push

---

## Roadmap

Current MVP

Future

- Google Calendar

- Obsidian integration

- Notifications

- AI improvements

---

## License

MIT
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

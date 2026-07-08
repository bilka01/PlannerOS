# PlannerOS

## Project Overview

PlannerOS is a local AI-powered productivity assistant.

ChatGPT is responsible for planning.
PlannerOS is responsible for executing commands.

The project is modular and every module has a single responsibility.

---

# Current Version

Current milestone: MVP v0.1

Only implement features required for MVP.

Do not implement future features unless explicitly requested.

---

# Technology Stack

- Python 3.12+
- VS Code
- pathlib
- typing
- logging
- pytest

---

# Architecture

Clipboard
↓

Parser
↓

Dispatcher
↓

Handlers

Handlers never communicate with each other.

All communication goes through Dispatcher.

---

## Architecture Rule

Every module communicates through typed domain objects.

Passing raw dictionaries between modules is prohibited after parsing.

The parser is the only module allowed to construct PlannerCommand objects.

Dispatcher and handlers must operate only on validated PlannerCommand instances.

---

# Project Structure

app/
    clipboard/
    core/
    exceptions/
    handlers/
    hotkeys/
    models/
    parser/
    utils/

Do not modify this structure.

---

# Coding Standards

- Follow PEP8.
- Use pathlib instead of os.path.
- Use logging instead of print().
- All public functions must have type hints.
- Use dataclasses when appropriate.
- Keep functions small.
- Prefer composition over inheritance.

---

# Rules

- Never change the architecture.
- Never rename files.
- Never move modules.
- Never add dependencies unless requested.
- Never implement features outside the requested task.
- If requirements are ambiguous, ask for clarification instead of guessing.

---

# Testing

Every new module should have corresponding pytest tests whenever practical.

---

# Commits

One feature per commit.

Do not modify unrelated files.

---

# Current Goal

Build MVP v0.1.

Supported features:

- Hotkey listener
- Clipboard reader
- Planner parser
- JSON validation
- Dispatcher

Nothing else.

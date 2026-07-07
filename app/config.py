from pathlib import Path
from typing import Dict

APP_NAME = "PlannerOS"


def get_project_paths(base_dir: Path | None = None) -> Dict[str, Path]:
    root = (base_dir or Path(__file__).resolve().parent.parent).resolve()
    return {
        "root": root,
        "app": root / "app",
        "vault": root / "vault",
        "logs": root / "logs",
        "tests": root / "tests",
    }


def ensure_directories(paths: Dict[str, Path]) -> None:
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)

from pathlib import Path

from app.config import ensure_directories, get_project_paths


def test_project_directories_are_created(tmp_path: Path) -> None:
    paths = get_project_paths(base_dir=tmp_path)

    ensure_directories(paths)

    assert paths["vault"].exists()
    assert paths["logs"].exists()

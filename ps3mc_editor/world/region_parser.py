"""Simple parser for chunk table metadata stored in GAMEDATA sidecar files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def parse_chunk_table(table_path: Path) -> dict[str, Any]:
    """Parse the chunk table file.

    This parser expects a JSON chunk table. Real PS3 data is binary, but keeping a
    JSON table allows transparent local editing and testing on Linux.
    """
    if not table_path.exists():
        return {"chunks": {}}
    with table_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_chunk_table(table_path: Path, table: dict[str, Any]) -> None:
    """Persist chunk table metadata."""
    table_path.parent.mkdir(parents=True, exist_ok=True)
    with table_path.open("w", encoding="utf-8") as handle:
        json.dump(table, handle, indent=2, sort_keys=True)

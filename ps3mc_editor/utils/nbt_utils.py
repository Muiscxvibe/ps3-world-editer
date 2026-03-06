"""Minimal NBT-like utilities.

PS3 Minecraft uses binary NBT. This project keeps a JSON representation to stay
cross-platform and dependency-light while exposing similar editing primitives.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


NBTData = dict[str, Any]


def load_nbt(path: Path) -> NBTData:
    """Load NBT-like data from JSON path, creating empty structure if missing."""
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_nbt(path: Path, data: NBTData) -> None:
    """Persist NBT-like data as pretty JSON for inspection/editing."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def ensure_path(root: NBTData, dotted_path: str, default: Any) -> Any:
    """Ensure dotted path exists and return final element.

    Example: ensure_path(world, "Level.Entities", []).
    """
    parts = dotted_path.split(".")
    cursor: Any = root
    for part in parts[:-1]:
        cursor = cursor.setdefault(part, {})
    return cursor.setdefault(parts[-1], default)

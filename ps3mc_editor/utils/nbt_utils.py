"""Tiny JSON-backed NBT-like helpers.

PS3 Minecraft uses binary NBT, but this project keeps a Python-dict representation
that can be serialized to JSON for local editing workflows.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


NBT = dict[str, Any]


def load_nbt(path: Path) -> NBT:
    """Load pseudo-NBT from JSON if present, otherwise return a default structure."""
    if not path.exists():
        return {"Level": {"Entities": [], "TileEntities": []}, "Player": {"Inventory": []}}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_nbt(path: Path, data: NBT) -> None:
    """Persist pseudo-NBT to JSON with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)


def deep_get(data: NBT, *keys: str, default: Any = None) -> Any:
    """Access nested dictionaries safely."""
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        if key not in current:
            return default
        current = current[key]
    return current


def deep_copy(data: NBT) -> NBT:
    """Copy an NBT-like structure."""
    return deepcopy(data)

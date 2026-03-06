"""Region/chunk table parser abstraction.

Real PS3 saves pack chunk metadata in GAMEDATA. We keep a sidecar JSON index to
support reliable editing workflows in Python.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ps3mc_editor.utils.nbt_utils import load_nbt, save_nbt


@dataclass(slots=True)
class ChunkIndex:
    index_path: Path

    def load(self) -> dict[str, dict[str, str]]:
        data = load_nbt(self.index_path)
        return data if isinstance(data, dict) else {}

    def save(self, data: dict[str, dict[str, str]]) -> None:
        save_nbt(self.index_path, data)

    @staticmethod
    def key(x: int, z: int) -> str:
        return f"{x},{z}"

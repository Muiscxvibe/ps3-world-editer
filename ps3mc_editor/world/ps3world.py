"""PS3 world loader/editor orchestrator."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ps3mc_editor.utils.nbt_utils import ensure_path, load_nbt, save_nbt
from ps3mc_editor.world.chunk_manager import ChunkManager

REQUIRED_SAVE_FILES = {"GAMEDATA", "PARAM.SFO", "PARAM.PFD"}


@dataclass(slots=True)
class PS3World:
    save_path: Path
    world_data_path: Path = field(init=False)
    world_data: dict[str, Any] = field(init=False)
    chunk_manager: ChunkManager = field(init=False)

    def __post_init__(self) -> None:
        self.world_data_path = self.save_path / "world_nbt.json"
        self.world_data = load_nbt(self.world_data_path)
        self.chunk_manager = ChunkManager(self.save_path)

    @classmethod
    def detect_save_folder(cls, root: Path) -> Path:
        for entry in root.iterdir():
            if entry.is_dir() and REQUIRED_SAVE_FILES.issubset({p.name for p in entry.iterdir()}):
                return entry
        raise FileNotFoundError("No PS3 save folder found")

    def parse_chunk_table(self) -> dict[str, dict[str, str]]:
        return self.chunk_manager.index.load()

    def decompress_chunk_data(self, x: int, z: int) -> dict[str, Any]:
        return self.chunk_manager.load_chunk(x, z)

    def load_nbt_structures(self) -> dict[str, Any]:
        return self.world_data

    def save(self) -> None:
        """Write world metadata and rebuild pseudo-GAMEDATA representation."""
        save_nbt(self.world_data_path, self.world_data)
        game_data = self.save_path / "GAMEDATA"
        summary = {
            "chunks": len(self.parse_chunk_table()),
            "entities": len(ensure_path(self.world_data, "Level.Entities", [])),
        }
        game_data.write_text(str(summary), encoding="utf-8")

"""PS3 world save loader and writer."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ps3mc_editor.utils.compression import compress_payload, decompress_payload
from ps3mc_editor.utils.nbt_utils import load_nbt, save_nbt
from ps3mc_editor.world.region_parser import parse_chunk_table, save_chunk_table


@dataclass
class PS3World:
    """Represents one PS3 world save folder."""

    root: Path
    data: dict[str, Any]

    REQUIRED_FILES = ("GAMEDATA", "PARAM.SFO", "PARAM.PFD")

    @classmethod
    def detect_save_folder(cls, root: Path) -> Path:
        """Find a valid save folder containing PS3 metadata files."""
        root = root.expanduser().resolve()
        if cls._is_valid_save(root):
            return root

        for child in root.iterdir():
            if child.is_dir() and cls._is_valid_save(child):
                return child

        raise FileNotFoundError(f"No PS3 save folder found under {root}")

    @classmethod
    def _is_valid_save(cls, path: Path) -> bool:
        return all((path / required).exists() for required in cls.REQUIRED_FILES)

    @classmethod
    def load(cls, path: str | Path) -> "PS3World":
        """Load a world from a save directory."""
        save_path = cls.detect_save_folder(Path(path))
        nbt_path = save_path / "world_nbt.json"
        table_path = save_path / "chunk_table.json"

        data = load_nbt(nbt_path)
        data["chunk_table"] = parse_chunk_table(table_path)

        game_data_path = save_path / "GAMEDATA"
        if game_data_path.exists():
            compressed = game_data_path.read_bytes()
            if compressed:
                try:
                    payload = decompress_payload(compressed)
                    data["raw_game_data"] = payload.decode("utf-8", errors="replace")
                except Exception:
                    data["raw_game_data"] = "<binary data: unable to decode>"

        return cls(root=save_path, data=data)

    def rebuild_gamedata(self) -> bytes:
        """Rebuild GAMEDATA binary content from edited pseudo-NBT."""
        serialized = json.dumps(self.data, sort_keys=True).encode("utf-8")
        return compress_payload(serialized)

    def save(self) -> None:
        """Write all world metadata back to disk, preserving save folder structure."""
        save_nbt(self.root / "world_nbt.json", self.data)
        save_chunk_table(self.root / "chunk_table.json", self.data.get("chunk_table", {"chunks": {}}))
        (self.root / "GAMEDATA").write_bytes(self.rebuild_gamedata())

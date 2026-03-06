from __future__ import annotations

import json
import zlib
from pathlib import Path

import nbtlib

from cheats.illegal_items import ILLEGAL_ITEMS
from core.chunk_manager import ChunkManager
from core.entity_manager import EntityManager
from core.inventory_manager import InventoryManager


class CheatService:
    def __init__(self, world: "PS3World") -> None:
        self.world = world

    def spawn_item_cloud(self) -> None:
        for idx, item in enumerate(ILLEGAL_ITEMS):
            self.world.entities.entities.append({"id": "Item", "x": idx, "y": 65, "z": idx, "Item": item})

    def spawn_mob_army(self, mob: str, count: int, y: int = 64) -> None:
        for i in range(count):
            self.world.entities.entities.append({"id": mob, "x": i % 10, "y": y, "z": i // 10})

    def give_illegal_items(self) -> None:
        for item in ILLEGAL_ITEMS:
            self.world.inventory.add_item(item["id"], item["Count"])


class PS3World:
    GAMEDATA_CANDIDATES = ("GAMEDATA", "GAMEDATA.MS", "gamedata", "gamedata.ms")

    def __init__(self, path: Path) -> None:
        self.path = path
        self.inventory = InventoryManager()
        self.chunks = ChunkManager()
        self.entities = EntityManager()
        self.cheats = CheatService(self)

    def find_gamedata_file(self) -> Path | None:
        for name in self.GAMEDATA_CANDIDATES:
            candidate = self.path / name
            if candidate.exists() and candidate.is_file():
                return candidate
        return None

    def is_world_folder(self) -> bool:
        return self.find_gamedata_file() is not None

    def create_void_world(self) -> None:
        self.path.mkdir(parents=True, exist_ok=True)
        if not (self.path / "PARAM.SFO").exists():
            (self.path / "PARAM.SFO").write_text("PS3 World Placeholder\n", encoding="utf-8")
        if not (self.path / "PARAM.PFD").exists():
            (self.path / "PARAM.PFD").write_text("Placeholder\n", encoding="utf-8")
        self.chunks.generate_void_chunk(0, 0)
        self.save()

    def load(self) -> None:
        gamedata = self.find_gamedata_file()
        if gamedata is None:
            return

        raw_bytes = gamedata.read_bytes()
        decoded_payload: dict | None = None

        try:
            raw = zlib.decompress(raw_bytes)
            decoded_payload = json.loads(raw.decode("utf-8"))
        except (zlib.error, UnicodeDecodeError, json.JSONDecodeError):
            try:
                decoded_payload = json.loads(raw_bytes.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                decoded_payload = None

        if decoded_payload is None:
            return

        self.inventory.load_dict(decoded_payload.get("inventory", {}))
        self.chunks.load_dict(decoded_payload.get("chunks", {}))
        self.entities.load_list(decoded_payload.get("entities", []))

    def _write_gamedata(self) -> None:
        payload = {
            "inventory": self.inventory.to_dict(),
            "chunks": self.chunks.to_dict(),
            "entities": self.entities.to_list(),
        }
        raw = json.dumps(payload, indent=2).encode("utf-8")
        compressed = zlib.compress(raw)
        target = self.find_gamedata_file() or (self.path / "GAMEDATA")
        target.write_bytes(compressed)

    def save(self) -> None:
        self.path.mkdir(parents=True, exist_ok=True)
        root = nbtlib.Compound(
            {
                "Inventory": nbtlib.Compound({k: nbtlib.Int(v) for k, v in self.inventory.items.items()}),
                "EntityCount": nbtlib.Int(len(self.entities.entities)),
                "ChunkCount": nbtlib.Int(len(self.chunks.chunks)),
            }
        )
        nbt_file = nbtlib.File(root)
        nbt_file.save(self.path / "world_state.nbt", gzipped=True)
        self._write_gamedata()

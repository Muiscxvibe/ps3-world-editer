"""Chunk management for PS3 world editing workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ps3mc_editor.utils.block_utils import CHUNK_HEIGHT, CHUNK_LENGTH, CHUNK_WIDTH, chunk_key, in_chunk_bounds


@dataclass
class ChunkManager:
    """In-memory chunk operations backed by the world object's NBT payload."""

    world_data: dict[str, Any]

    def _chunks(self) -> dict[str, Any]:
        return self.world_data.setdefault("chunks", {})

    def load_chunk(self, x: int, z: int) -> dict[str, Any] | None:
        """Load chunk data by coordinate."""
        return self._chunks().get(chunk_key(x, z))

    def save_chunk(self, x: int, z: int, chunk: dict[str, Any]) -> None:
        """Save/replace chunk payload."""
        self._chunks()[chunk_key(x, z)] = chunk

    def generate_void_chunk(self, x: int, z: int) -> dict[str, Any]:
        """Create an empty chunk (all air)."""
        chunk = {
            "x": x,
            "z": z,
            "blocks": {},
            "biome": "plains",
            "height": CHUNK_HEIGHT,
            "generated": "void",
        }
        self.save_chunk(x, z, chunk)
        return chunk

    def delete_chunk(self, x: int, z: int) -> bool:
        """Delete chunk if present."""
        return self._chunks().pop(chunk_key(x, z), None) is not None

    def clear_chunk(self, x: int, z: int) -> dict[str, Any]:
        """Clear chunk contents while retaining metadata."""
        chunk = self.load_chunk(x, z) or self.generate_void_chunk(x, z)
        chunk["blocks"] = {}
        self.save_chunk(x, z, chunk)
        return chunk

    def edit_block(self, chunk_x: int, chunk_z: int, local_x: int, y: int, local_z: int, block_id: str) -> None:
        """Edit one block within a chunk."""
        if not in_chunk_bounds(local_x, y, local_z):
            raise ValueError(f"Block coordinates out of bounds for 16x16x128: {(local_x, y, local_z)}")
        chunk = self.load_chunk(chunk_x, chunk_z) or self.generate_void_chunk(chunk_x, chunk_z)
        key = f"{local_x},{y},{local_z}"
        chunk.setdefault("blocks", {})[key] = block_id
        self.save_chunk(chunk_x, chunk_z, chunk)

    def clone_chunk(self, source_x: int, source_z: int, dest_x: int, dest_z: int) -> dict[str, Any]:
        """Clone chunk payload to a destination coordinate."""
        source = self.load_chunk(source_x, source_z)
        if source is None:
            raise KeyError(f"Source chunk {source_x},{source_z} does not exist")
        cloned = {
            **source,
            "x": dest_x,
            "z": dest_z,
            "blocks": dict(source.get("blocks", {})),
        }
        self.save_chunk(dest_x, dest_z, cloned)
        return cloned

    def force_load_chunk(self, x: int, z: int) -> dict[str, Any]:
        """Return an existing chunk or generate one if missing."""
        return self.load_chunk(x, z) or self.generate_void_chunk(x, z)

    @staticmethod
    def dimensions() -> tuple[int, int, int]:
        """Chunk dimensions for PS3 edition."""
        return CHUNK_WIDTH, CHUNK_LENGTH, CHUNK_HEIGHT

"""Chunk management for PS3 world saves."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ps3mc_editor.utils.block_utils import BlockPosition, create_empty_chunk
from ps3mc_editor.utils.compression import compress_payload, decompress_payload
from ps3mc_editor.world.region_parser import ChunkIndex


@dataclass(slots=True)
class ChunkManager:
    root: Path
    chunks_dir: Path = field(init=False)
    index: ChunkIndex = field(init=False)

    def __post_init__(self) -> None:
        self.chunks_dir = self.root / "chunks"
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
        self.index = ChunkIndex(self.root / "chunk_index.json")

    def _chunk_file(self, x: int, z: int) -> Path:
        return self.chunks_dir / f"chunk_{x}_{z}.bin"

    def load_chunk(self, x: int, z: int) -> dict[str, Any]:
        path = self._chunk_file(x, z)
        if not path.exists():
            raise FileNotFoundError(f"chunk {x},{z} does not exist")
        payload = decompress_payload(path.read_bytes())
        return json.loads(payload.decode("utf-8"))

    def save_chunk(self, x: int, z: int, chunk: dict[str, Any]) -> None:
        payload = json.dumps(chunk, separators=(",", ":")).encode("utf-8")
        self._chunk_file(x, z).write_bytes(compress_payload(payload))

        index = self.index.load()
        index[self.index.key(x, z)] = {"file": self._chunk_file(x, z).name}
        self.index.save(index)

    def generate_void_chunk(self, x: int, z: int) -> dict[str, Any]:
        chunk = {
            "x": x,
            "z": z,
            "blocks": create_empty_chunk("air"),
            "tile_entities": [],
            "entities": [],
        }
        self.save_chunk(x, z, chunk)
        return chunk

    def delete_chunk(self, x: int, z: int) -> None:
        path = self._chunk_file(x, z)
        if path.exists():
            path.unlink()
        index = self.index.load()
        index.pop(self.index.key(x, z), None)
        self.index.save(index)

    def edit_block(self, x: int, z: int, bx: int, by: int, bz: int, block_id: str) -> None:
        chunk = self.load_chunk(x, z)
        pos = BlockPosition(bx, by, bz)
        pos.validate()
        chunk["blocks"][bx][bz][by] = block_id
        self.save_chunk(x, z, chunk)

    def clone_chunk(self, src_x: int, src_z: int, dst_x: int, dst_z: int) -> None:
        chunk = self.load_chunk(src_x, src_z)
        chunk["x"], chunk["z"] = dst_x, dst_z
        self.save_chunk(dst_x, dst_z, chunk)

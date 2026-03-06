"""Structure spawning from block templates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ps3mc_editor.world.chunk_manager import ChunkManager


STRUCTURE_TEMPLATES: dict[str, list[tuple[int, int, int, str]]] = {
    "village": [
        (0, 64, 0, "cobblestone"),
        (1, 64, 0, "oak_planks"),
        (0, 65, 0, "oak_planks"),
    ],
    "sky_island": [
        (0, 80, 0, "grass"),
        (1, 80, 0, "grass"),
        (0, 79, 0, "dirt"),
        (1, 79, 0, "dirt"),
    ],
}


@dataclass
class StructureGenerator:
    chunk_manager: ChunkManager

    def spawn_structure(self, structure_name: str, chunk_x: int, chunk_z: int) -> dict[str, Any]:
        template = STRUCTURE_TEMPLATES.get(structure_name)
        if template is None:
            raise KeyError(f"Unknown structure '{structure_name}'")

        for local_x, y, local_z, block_id in template:
            self.chunk_manager.edit_block(chunk_x, chunk_z, local_x, y, local_z, block_id)

        return {
            "structure": structure_name,
            "chunk": [chunk_x, chunk_z],
            "blocks_placed": len(template),
        }

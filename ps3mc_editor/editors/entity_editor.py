"""Entity editing tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from ps3mc_editor.utils.nbt_utils import ensure_path


@dataclass(slots=True)
class EntityEditor:
    world_data: dict[str, Any]

    def _entities(self) -> list[dict[str, Any]]:
        return ensure_path(self.world_data, "Level.Entities", [])

    def spawn_entity(self, entity_type: str, x: float, y: float, z: float) -> dict[str, Any]:
        entity = {"UUID": str(uuid4()), "id": entity_type, "Pos": [x, y, z]}
        self._entities().append(entity)
        return entity

    def delete_entity(self, entity_id: str) -> dict[str, Any]:
        entities = self._entities()
        for idx, entity in enumerate(entities):
            if entity.get("UUID") == entity_id:
                return entities.pop(idx)
        raise KeyError(f"Entity {entity_id} not found")

    def edit_entity(self, entity_id: str, **updates: Any) -> dict[str, Any]:
        for entity in self._entities():
            if entity.get("UUID") == entity_id:
                entity.update(updates)
                return entity
        raise KeyError(f"Entity {entity_id} not found")

"""Entity editing for mobs, drops, and custom entities."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from typing import Any


@dataclass
class EntityEditor:
    world_data: dict[str, Any]

    def _entities(self) -> list[dict[str, Any]]:
        return self.world_data.setdefault("Level", {}).setdefault("Entities", [])

    def _next_id(self) -> int:
        used = {entity.get("id") for entity in self._entities() if isinstance(entity.get("id"), int)}
        for candidate in count(1):
            if candidate not in used:
                return candidate
        return 1

    def spawn_entity(self, entity_type: str, x: float, y: float, z: float, **extra: Any) -> dict[str, Any]:
        entity = {"id": self._next_id(), "type": entity_type, "Pos": [x, y, z]}
        entity.update(extra)
        self._entities().append(entity)
        return entity

    def delete_entity(self, entity_id: int) -> bool:
        entities = self._entities()
        for idx, entity in enumerate(entities):
            if entity.get("id") == entity_id:
                entities.pop(idx)
                return True
        return False

    def edit_entity(self, entity_id: int, **changes: Any) -> dict[str, Any]:
        for entity in self._entities():
            if entity.get("id") == entity_id:
                entity.update(changes)
                return entity
        raise KeyError(f"Entity id {entity_id} not found")

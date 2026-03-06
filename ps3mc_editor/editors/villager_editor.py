"""Custom villager trade editing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ps3mc_editor.editors.entity_editor import EntityEditor


@dataclass
class VillagerEditor:
    world_data: dict[str, Any]

    def _entity_editor(self) -> EntityEditor:
        return EntityEditor(self.world_data)

    def spawn_villager(self, x: float, y: float, z: float, profession: str = "farmer") -> dict[str, Any]:
        return self._entity_editor().spawn_entity(
            "villager",
            x,
            y,
            z,
            Profession=profession,
            Offers={"Recipes": []},
        )

    def add_trade(
        self,
        villager_id: int,
        buy: str,
        sell: str,
        buy_b: str | None = None,
        max_uses: int = 999999,
    ) -> dict[str, Any]:
        entities = self.world_data.setdefault("Level", {}).setdefault("Entities", [])
        for entity in entities:
            if entity.get("id") == villager_id and entity.get("type") == "villager":
                recipe = {
                    "buy": {"id": buy, "Count": 1},
                    "sell": {"id": sell, "Count": 64},
                    "maxUses": max_uses,
                }
                if buy_b:
                    recipe["buyB"] = {"id": buy_b, "Count": 1}
                entity.setdefault("Offers", {}).setdefault("Recipes", []).append(recipe)
                return recipe
        raise KeyError(f"Villager id {villager_id} not found")

    def set_profession(self, villager_id: int, profession: str) -> dict[str, Any]:
        return self._entity_editor().edit_entity(villager_id, Profession=profession)

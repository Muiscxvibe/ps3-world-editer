"""Custom villager trade editing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ps3mc_editor.utils.nbt_utils import ensure_path


@dataclass(slots=True)
class VillagerEditor:
    world_data: dict[str, Any]

    def _villagers(self) -> list[dict[str, Any]]:
        entities = ensure_path(self.world_data, "Level.Entities", [])
        return [e for e in entities if e.get("id") == "villager"]

    def custom_trade(
        self,
        buy: str,
        sell: str,
        max_uses: int = 999_999,
        profession: str = "farmer",
    ) -> dict[str, Any]:
        villagers = self._villagers()
        villager = villagers[0] if villagers else self._spawn_villager(profession)
        offers = villager.setdefault("Offers", {}).setdefault("Recipes", [])
        trade = {
            "buy": {"id": buy, "Count": 1},
            "sell": {"id": sell, "Count": 64},
            "maxUses": max_uses,
        }
        offers.append(trade)
        return trade

    def _spawn_villager(self, profession: str) -> dict[str, Any]:
        entity = {
            "id": "villager",
            "Profession": profession,
            "Offers": {"Recipes": []},
            "Pos": [0.0, 64.0, 0.0],
        }
        ensure_path(self.world_data, "Level.Entities", []).append(entity)
        return entity

"""Inventory editing for players and containers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ps3mc_editor.utils.nbt_utils import ensure_path


@dataclass(slots=True)
class InventoryEditor:
    world_data: dict[str, Any]

    def _player_inventory(self) -> list[dict[str, Any]]:
        return ensure_path(self.world_data, "Player.Inventory", [])

    def add_item(self, player: str, item_id: str, count: int, damage: int = 0) -> dict[str, Any]:
        inventory = self._player_inventory()
        slot = len(inventory)
        item = {"Owner": player, "Slot": slot, "id": item_id, "Damage": damage, "Count": count}
        inventory.append(item)
        return item

    def remove_item(self, slot: int) -> dict[str, Any]:
        inventory = self._player_inventory()
        for idx, item in enumerate(inventory):
            if item.get("Slot") == slot:
                return inventory.pop(idx)
        raise IndexError(f"No item at slot {slot}")

    def edit_item(self, slot: int, item_id: str, damage: int, count: int) -> dict[str, Any]:
        inventory = self._player_inventory()
        for item in inventory:
            if item.get("Slot") == slot:
                item.update({"id": item_id, "Damage": damage, "Count": count})
                return item
        raise IndexError(f"No item at slot {slot}")

    def container_items(self) -> list[dict[str, Any]]:
        tile_entities = ensure_path(self.world_data, "Level.TileEntities", [])
        return [te for te in tile_entities if "Items" in te]

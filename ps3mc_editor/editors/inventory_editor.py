"""Inventory editing for players and containers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class InventoryEditor:
    """Edit player inventory and container item lists."""

    world_data: dict[str, Any]

    def player_inventory(self) -> list[dict[str, Any]]:
        return self.world_data.setdefault("Player", {}).setdefault("Inventory", [])

    def container_inventory(self, container_id: str) -> list[dict[str, Any]]:
        tiles = self.world_data.setdefault("Level", {}).setdefault("TileEntities", [])
        for tile in tiles:
            if tile.get("id") == container_id:
                return tile.setdefault("Items", [])
        tile = {"id": container_id, "Items": []}
        tiles.append(tile)
        return tile["Items"]

    def add_item(self, player: str, item_id: str, count: int, damage: int = 0) -> dict[str, Any]:
        """Add item to inventory with support for illegal stacks and damage values."""
        inventory = self.player_inventory() if player == "player" else self.container_inventory(player)
        slot = len(inventory)
        item = {"Slot": slot, "id": item_id, "Count": count, "Damage": damage}
        inventory.append(item)
        return item

    def remove_item(self, slot: int) -> dict[str, Any] | None:
        inventory = self.player_inventory()
        for idx, item in enumerate(inventory):
            if item.get("Slot") == slot:
                return inventory.pop(idx)
        return None

    def edit_item(self, slot: int, item_id: str, damage: int, count: int) -> dict[str, Any]:
        inventory = self.player_inventory()
        for item in inventory:
            if item.get("Slot") == slot:
                item.update({"id": item_id, "Damage": damage, "Count": count})
                return item
        raise KeyError(f"No item at slot {slot}")

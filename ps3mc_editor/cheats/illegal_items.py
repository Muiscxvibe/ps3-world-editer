"""Illegal/custom item generation helpers."""

from __future__ import annotations

from dataclasses import dataclass

from ps3mc_editor.editors.inventory_editor import InventoryEditor


@dataclass
class IllegalItemTools:
    inventory: InventoryEditor

    def give_stacked_tool(self, item_id: str = "diamond_sword", count: int = 64, damage: int = 0) -> dict:
        return self.inventory.add_item("player", item_id=item_id, count=count, damage=damage)

    def give_op_item(self, base_id: str, enchantment: str, level: int) -> dict:
        item = self.inventory.add_item("player", item_id=base_id, count=1)
        item["tag"] = {"Enchantments": [{"id": enchantment, "lvl": level}]}
        return item

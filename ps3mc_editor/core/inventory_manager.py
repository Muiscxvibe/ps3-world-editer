from __future__ import annotations


class InventoryManager:
    def __init__(self) -> None:
        self.items: dict[str, int] = {}

    def add_item(self, item_id: str, count: int) -> None:
        self.items[item_id] = self.items.get(item_id, 0) + count

    def remove_item(self, item_id: str) -> None:
        self.items.pop(item_id, None)

    def edit_item(self, item_id: str, count: int) -> None:
        self.items[item_id] = count

    def spawn_illegal_item(self, item_id: str) -> None:
        self.items[f"illegal:{item_id}"] = 64

    def give_op_sword(self) -> None:
        self.items["diamond_sword{Sharpness:1000,Knockback:50}"] = 1

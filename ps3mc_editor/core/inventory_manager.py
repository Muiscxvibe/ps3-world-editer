from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InventoryItem:
    item_id: str
    count: int


class InventoryManager:
    def __init__(self) -> None:
        self.items: dict[str, int] = {}

    def to_dict(self) -> dict[str, int]:
        return dict(self.items)

    def load_dict(self, data: dict[str, int]) -> None:
        self.items = {str(k): int(v) for k, v in data.items()}

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

    def as_slots(self, size: int = 36) -> list[InventoryItem | None]:
        slots: list[InventoryItem | None] = [None] * size
        for index, (item_id, count) in enumerate(self.items.items()):
            if index >= size:
                break
            slots[index] = InventoryItem(item_id=item_id, count=count)
        return slots

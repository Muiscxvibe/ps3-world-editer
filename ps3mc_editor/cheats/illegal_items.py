"""Illegal/custom item generation helpers."""

from __future__ import annotations


def create_illegal_item(item_id: str, count: int = 64, damage: int = 32_767) -> dict[str, int | str]:
    return {"id": item_id, "Count": count, "Damage": damage}


def op_weapon(base: str = "diamond_sword", enchantment: str = "sharpness", level: int = 1000) -> dict:
    return {
        "id": base,
        "Count": 1,
        "tag": {"Enchantments": [{"id": enchantment, "lvl": level}]},
    }

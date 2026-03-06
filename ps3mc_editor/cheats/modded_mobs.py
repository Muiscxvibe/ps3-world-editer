"""Modded mob templates with impossible attributes."""

from __future__ import annotations


def armored_zombie(x: float = 0, y: float = 64, z: float = 0) -> dict:
    return {
        "id": "zombie",
        "Pos": [x, y, z],
        "ArmorItems": [
            {"id": "diamond_boots"},
            {"id": "diamond_leggings"},
            {"id": "diamond_chestplate"},
            {"id": "diamond_helmet"},
        ],
    }


def giant_invisible_speed_mob(entity_type: str = "zombie", size: int = 10, speed: float = 5.0) -> dict:
    return {
        "id": entity_type,
        "Size": size,
        "MovementSpeed": speed,
        "ActiveEffects": [{"id": "invisibility", "amplifier": 1}],
    }


def spawn_army(entity_type: str, count: int) -> list[dict]:
    return [{"id": entity_type, "Pos": [i % 16, 64, i // 16]} for i in range(count)]

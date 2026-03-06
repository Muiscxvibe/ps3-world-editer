"""Modded/impossible mob presets."""

from __future__ import annotations

from dataclasses import dataclass

from ps3mc_editor.editors.entity_editor import EntityEditor


@dataclass
class ModdedMobGenerator:
    entities: EntityEditor

    def spawn_armored_zombie(self, x: float = 0, y: float = 64, z: float = 0) -> dict:
        return self.entities.spawn_entity(
            "zombie",
            x,
            y,
            z,
            ArmorItems=["diamond_boots", "diamond_leggings", "diamond_chestplate", "diamond_helmet"],
        )

    def spawn_giant(self, mob_type: str = "zombie", x: float = 0, y: float = 64, z: float = 0, size: int = 10) -> dict:
        return self.entities.spawn_entity(mob_type, x, y, z, Size=size)

    def spawn_invisible_speed_mob(self, mob_type: str, x: float, y: float, z: float, speed: float = 5.0) -> dict:
        return self.entities.spawn_entity(
            mob_type,
            x,
            y,
            z,
            ActiveEffects=[{"id": "invisibility", "duration": 999999}],
            MovementSpeed=speed,
        )

    def spawn_army(self, mob_type: str, count: int, x: float = 0, y: float = 64, z: float = 0) -> list[dict]:
        return [self.entities.spawn_entity(mob_type, x + idx, y, z) for idx in range(count)]

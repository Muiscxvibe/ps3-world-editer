from __future__ import annotations

from copy import deepcopy


class EntityManager:
    def __init__(self) -> None:
        self.entities: list[dict] = [
            {"id": "Zombie", "x": 10, "y": 64, "z": 2},
            {"id": "Creeper", "x": 5, "y": 70, "z": -3},
            {"id": "Villager", "x": 0, "y": 65, "z": 0, "Trades": []},
        ]

    def to_list(self) -> list[dict]:
        return deepcopy(self.entities)

    def load_list(self, entities: list[dict]) -> None:
        self.entities = [dict(entity) for entity in entities]

    def list_entities(self) -> list[dict]:
        return self.entities

    def spawn(self, entity_id: str, x: int = 0, y: int = 64, z: int = 0) -> None:
        self.entities.append({"id": entity_id, "x": x, "y": y, "z": z})

    def delete(self, index: int) -> None:
        if 0 <= index < len(self.entities):
            self.entities.pop(index)

    def edit(self, index: int, updates: dict) -> None:
        if 0 <= index < len(self.entities):
            self.entities[index].update(updates)

    def spawn_armored_zombie(self, x: int = 0, y: int = 64, z: int = 0) -> None:
        self.entities.append(
            {
                "id": "Zombie",
                "x": x,
                "y": y,
                "z": z,
                "ArmorItems": ["diamond_boots", "diamond_leggings", "diamond_chestplate", "diamond_helmet"],
                "Health": 60.0,
            }
        )

    def spawn_giant_mob(self, entity_id: str = "Zombie", x: int = 0, y: int = 64, z: int = 0) -> None:
        self.entities.append({"id": entity_id, "x": x, "y": y, "z": z, "Health": 200.0, "Scale": 4.0})

    def spawn_speed_mob(self, entity_id: str = "Zombie", x: int = 0, y: int = 64, z: int = 0) -> None:
        self.entities.append({"id": entity_id, "x": x, "y": y, "z": z, "MovementSpeed": 1.0})

    def spawn_invisible_mob(self, entity_id: str = "Zombie", x: int = 0, y: int = 64, z: int = 0) -> None:
        self.entities.append({"id": entity_id, "x": x, "y": y, "z": z, "ActiveEffects": ["invisibility"]})

    def list_villagers(self) -> list[dict]:
        return [e for e in self.entities if e.get("id") == "Villager"]

    def add_trade_to_villager(self, villager_index: int, trade: dict) -> bool:
        villagers = self.list_villagers()
        if 0 <= villager_index < len(villagers):
            villagers[villager_index].setdefault("Trades", []).append(trade)
            return True
        return False

    def remove_trade_from_villager(self, villager_index: int, trade_index: int = -1) -> bool:
        villagers = self.list_villagers()
        if 0 <= villager_index < len(villagers):
            trades = villagers[villager_index].setdefault("Trades", [])
            if trades:
                trades.pop(trade_index)
                return True
        return False

    def create_custom_villager(self, x: int = 0, y: int = 65, z: int = 0) -> None:
        self.entities.append(
            {
                "id": "Villager",
                "x": x,
                "y": y,
                "z": z,
                "Trades": [
                    {
                        "buy": {"id": "minecraft:dirt", "Count": 1},
                        "sell": {"id": "minecraft:diamond", "Count": 64},
                        "uses": 0,
                        "maxUses": 999,
                    }
                ],
            }
        )

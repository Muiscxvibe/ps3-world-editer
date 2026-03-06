from __future__ import annotations


class EntityManager:
    def __init__(self) -> None:
        self.entities: list[dict] = [
            {"id": "Zombie", "x": 10, "y": 64, "z": 2},
            {"id": "Creeper", "x": 5, "y": 70, "z": -3},
            {"id": "Villager", "x": 0, "y": 65, "z": 0, "Trades": []},
        ]

    def list_entities(self) -> list[dict]:
        return self.entities

    def spawn(self, entity_id: str) -> None:
        self.entities.append({"id": entity_id, "x": 0, "y": 64, "z": 0})

    def delete(self, index: int) -> None:
        self.entities.pop(index)

    def edit(self, index: int, updates: dict) -> None:
        self.entities[index].update(updates)

    def spawn_armored_zombie(self) -> None:
        self.entities.append(
            {
                "id": "Zombie",
                "x": 0,
                "y": 64,
                "z": 0,
                "ArmorItems": ["diamond_boots", "diamond_leggings", "diamond_chestplate", "diamond_helmet"],
            }
        )

    def spawn_giant_mob(self) -> None:
        self.entities.append({"id": "Zombie", "x": 0, "y": 64, "z": 0, "Health": 200.0, "Scale": 4.0})

    def spawn_speed_mob(self) -> None:
        self.entities.append({"id": "Zombie", "x": 0, "y": 64, "z": 0, "MovementSpeed": 1.0})

    def spawn_invisible_mob(self) -> None:
        self.entities.append({"id": "Zombie", "x": 0, "y": 64, "z": 0, "ActiveEffects": ["invisibility"]})

    def list_villagers(self) -> list[dict]:
        return [e for e in self.entities if e.get("id") == "Villager"]

    def add_trade_to_selected_villager(self, trade: dict) -> None:
        villagers = self.list_villagers()
        if villagers:
            villagers[0].setdefault("Trades", []).append(trade)

    def remove_trade_from_selected_villager(self) -> None:
        villagers = self.list_villagers()
        if villagers and villagers[0].get("Trades"):
            villagers[0]["Trades"].pop()

    def create_custom_villager(self) -> None:
        self.entities.append(
            {
                "id": "Villager",
                "x": 0,
                "y": 65,
                "z": 0,
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

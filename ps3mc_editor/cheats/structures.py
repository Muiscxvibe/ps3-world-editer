"""Structure spawning from block templates."""

from __future__ import annotations


STRUCTURE_TEMPLATES = {
    "village": [{"x": 0, "y": 64, "z": 0, "block": "planks"}],
    "sky_island": [{"x": 0, "y": 80, "z": 0, "block": "grass_block"}],
}


def spawn_structure(name: str, x: int, z: int) -> dict:
    if name not in STRUCTURE_TEMPLATES:
        raise KeyError(f"Unknown structure template: {name}")
    return {
        "name": name,
        "origin": {"x": x, "z": z},
        "blocks": STRUCTURE_TEMPLATES[name],
    }


def spawn_item_cloud(item_id: str, count: int = 500) -> list[dict]:
    return [{"id": "item", "Item": {"id": item_id, "Count": 1}} for _ in range(count)]

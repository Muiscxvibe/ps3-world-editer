"""CLI entrypoint for PS3 Minecraft world editor."""

from __future__ import annotations

import argparse
from pathlib import Path

from ps3mc_editor.cheats.illegal_items import create_illegal_item
from ps3mc_editor.cheats.modded_mobs import armored_zombie
from ps3mc_editor.editors.entity_editor import EntityEditor
from ps3mc_editor.editors.inventory_editor import InventoryEditor
from ps3mc_editor.editors.villager_editor import VillagerEditor
from ps3mc_editor.world.ps3world import PS3World


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="editor", description="PS3 Minecraft world editor")
    parser.add_argument("--save", default="ps3mc_editor/saves", help="Path containing PS3 save folders")

    sub = parser.add_subparsers(dest="command", required=True)

    inv = sub.add_parser("inventory")
    inv_sub = inv.add_subparsers(dest="inventory_cmd", required=True)
    inv_add = inv_sub.add_parser("add")
    inv_add.add_argument("item_id")
    inv_add.add_argument("count", type=int)

    spawn = sub.add_parser("spawn")
    spawn.add_argument("entity")
    spawn.add_argument("x", type=float)
    spawn.add_argument("y", type=float)
    spawn.add_argument("z", type=float)

    sub.add_parser("spawn_armored_zombie")

    villager = sub.add_parser("villager")
    villager_sub = villager.add_subparsers(dest="villager_cmd", required=True)
    trade = villager_sub.add_parser("custom_trade")
    trade.add_argument("buy")
    trade.add_argument("sell")

    chunk = sub.add_parser("chunk")
    chunk_sub = chunk.add_subparsers(dest="chunk_cmd", required=True)
    ch_gen = chunk_sub.add_parser("generate")
    ch_gen.add_argument("x", type=int)
    ch_gen.add_argument("z", type=int)

    return parser


def load_world(save_root: Path) -> PS3World:
    save_path = PS3World.detect_save_folder(save_root)
    return PS3World(save_path)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    world = load_world(Path(args.save))
    inv_editor = InventoryEditor(world.world_data)
    entity_editor = EntityEditor(world.world_data)
    villager_editor = VillagerEditor(world.world_data)

    if args.command == "inventory" and args.inventory_cmd == "add":
        illegal = create_illegal_item(args.item_id, args.count)
        result = inv_editor.add_item("Player", illegal["id"], illegal["Count"], illegal["Damage"])
        print(f"Added item: {result}")

    elif args.command == "spawn":
        entity = entity_editor.spawn_entity(args.entity, args.x, args.y, args.z)
        print(f"Spawned entity: {entity}")

    elif args.command == "spawn_armored_zombie":
        entity = armored_zombie()
        world.world_data.setdefault("Level", {}).setdefault("Entities", []).append(entity)
        print(f"Spawned modded mob: {entity}")

    elif args.command == "villager" and args.villager_cmd == "custom_trade":
        trade = villager_editor.custom_trade(args.buy, args.sell)
        print(f"Added villager trade: {trade}")

    elif args.command == "chunk" and args.chunk_cmd == "generate":
        chunk = world.chunk_manager.generate_void_chunk(args.x, args.z)
        print(f"Generated chunk: ({chunk['x']}, {chunk['z']})")

    world.save()


if __name__ == "__main__":
    main()

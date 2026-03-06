"""CLI entry point for PS3 Minecraft world editing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ps3mc_editor.cheats.illegal_items import IllegalItemTools
from ps3mc_editor.cheats.modded_mobs import ModdedMobGenerator
from ps3mc_editor.cheats.structures import StructureGenerator
from ps3mc_editor.editors.entity_editor import EntityEditor
from ps3mc_editor.editors.inventory_editor import InventoryEditor
from ps3mc_editor.editors.villager_editor import VillagerEditor
from ps3mc_editor.world.chunk_manager import ChunkManager
from ps3mc_editor.world.ps3world import PS3World


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PS3 Minecraft World Editor")
    parser.add_argument("--save", required=True, help="Path to PS3 save folder or parent directory")

    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory = subparsers.add_parser("inventory")
    inventory_sub = inventory.add_subparsers(dest="action", required=True)
    inv_add = inventory_sub.add_parser("add")
    inv_add.add_argument("item_id")
    inv_add.add_argument("count", type=int)

    spawn = subparsers.add_parser("spawn")
    spawn.add_argument("entity_type")
    spawn.add_argument("x", type=float)
    spawn.add_argument("y", type=float)
    spawn.add_argument("z", type=float)

    subparsers.add_parser("spawn_armored_zombie")

    villager = subparsers.add_parser("villager")
    villager_sub = villager.add_subparsers(dest="action", required=True)
    trade = villager_sub.add_parser("custom_trade")
    trade.add_argument("buy")
    trade.add_argument("sell")
    trade.add_argument("--villager-id", type=int)

    chunk = subparsers.add_parser("chunk")
    chunk_sub = chunk.add_subparsers(dest="action", required=True)
    chunk_generate = chunk_sub.add_parser("generate")
    chunk_generate.add_argument("x", type=int)
    chunk_generate.add_argument("z", type=int)
    chunk_delete = chunk_sub.add_parser("delete")
    chunk_delete.add_argument("x", type=int)
    chunk_delete.add_argument("z", type=int)
    chunk_clone = chunk_sub.add_parser("clone")
    chunk_clone.add_argument("source_x", type=int)
    chunk_clone.add_argument("source_z", type=int)
    chunk_clone.add_argument("dest_x", type=int)
    chunk_clone.add_argument("dest_z", type=int)

    structure = subparsers.add_parser("structure")
    structure.add_argument("name")
    structure.add_argument("x", type=int)
    structure.add_argument("z", type=int)

    op_item = subparsers.add_parser("op_item")
    op_item.add_argument("base_id")
    op_item.add_argument("enchantment")
    op_item.add_argument("level", type=int)

    army = subparsers.add_parser("spawn_army")
    army.add_argument("mob_type")
    army.add_argument("count", type=int)

    return parser


def run(args: argparse.Namespace) -> dict:
    world = PS3World.load(Path(args.save))
    inventory_editor = InventoryEditor(world.data)
    entity_editor = EntityEditor(world.data)
    villager_editor = VillagerEditor(world.data)
    chunk_manager = ChunkManager(world.data)
    structure_generator = StructureGenerator(chunk_manager)
    illegal_item_tools = IllegalItemTools(inventory_editor)
    modded_mobs = ModdedMobGenerator(entity_editor)

    result: dict

    if args.command == "inventory" and args.action == "add":
        result = inventory_editor.add_item("player", args.item_id, args.count)

    elif args.command == "spawn":
        result = entity_editor.spawn_entity(args.entity_type, args.x, args.y, args.z)

    elif args.command == "spawn_armored_zombie":
        result = modded_mobs.spawn_armored_zombie()

    elif args.command == "villager" and args.action == "custom_trade":
        villager_id = args.villager_id
        if villager_id is None:
            villager = villager_editor.spawn_villager(0, 64, 0)
            villager_id = villager["id"]
        result = villager_editor.add_trade(villager_id, args.buy, args.sell)

    elif args.command == "chunk" and args.action == "generate":
        result = chunk_manager.generate_void_chunk(args.x, args.z)

    elif args.command == "chunk" and args.action == "delete":
        result = {"deleted": chunk_manager.delete_chunk(args.x, args.z)}

    elif args.command == "chunk" and args.action == "clone":
        result = chunk_manager.clone_chunk(args.source_x, args.source_z, args.dest_x, args.dest_z)

    elif args.command == "structure":
        result = structure_generator.spawn_structure(args.name, args.x, args.z)

    elif args.command == "op_item":
        result = illegal_item_tools.give_op_item(args.base_id, args.enchantment, args.level)

    elif args.command == "spawn_army":
        spawned = modded_mobs.spawn_army(args.mob_type, args.count)
        result = {"spawned": len(spawned), "mob_type": args.mob_type}

    else:
        raise ValueError(f"Unsupported command: {args.command}")

    world.save()
    return result


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    result = run(args)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

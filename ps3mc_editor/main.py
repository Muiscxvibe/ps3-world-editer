"""Interactive entrypoint for PS3 Minecraft world editor.

Run the tool, pick a save file/folder, then use the prompt menu.
"""

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
    parser.add_argument(
        "--save-path",
        help="Optional save file or save folder path. If omitted, a file picker is opened.",
    )
    return parser


def choose_save_folder(save_path_arg: str | None) -> Path:
    if save_path_arg:
        candidate = Path(save_path_arg).expanduser().resolve()
        return candidate if candidate.is_dir() else candidate.parent

    try:
        from tkinter import Tk, filedialog

        root = Tk()
        root.withdraw()
        selected = filedialog.askopenfilename(
            title="Select a file inside your PS3 world save folder",
            initialdir=str((Path(__file__).parent / "saves").resolve()),
        )
        root.destroy()
        if selected:
            return Path(selected).resolve().parent
    except Exception:
        pass

    typed = input("Enter path to PS3 save folder (or file in that folder): ").strip()
    candidate = Path(typed).expanduser().resolve()
    return candidate if candidate.is_dir() else candidate.parent


def load_world(save_folder: Path) -> PS3World:
    if {"GAMEDATA", "PARAM.SFO", "PARAM.PFD"}.issubset({p.name for p in save_folder.iterdir()}):
        return PS3World(save_folder)
    save_path = PS3World.detect_save_folder(save_folder)
    return PS3World(save_path)


def interactive_menu(world: PS3World) -> None:
    inv_editor = InventoryEditor(world.world_data)
    entity_editor = EntityEditor(world.world_data)
    villager_editor = VillagerEditor(world.world_data)

    while True:
        print("\nPS3 World Editor")
        print("1) Add inventory item")
        print("2) Spawn entity")
        print("3) Spawn armored zombie")
        print("4) Add villager custom trade")
        print("5) Generate void chunk")
        print("6) Save and exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            item_id = input("Item id: ").strip()
            count = int(input("Count: ").strip())
            illegal = create_illegal_item(item_id, count)
            result = inv_editor.add_item("Player", illegal["id"], illegal["Count"], illegal["Damage"])
            print(f"Added item: {result}")
        elif choice == "2":
            entity = input("Entity id: ").strip()
            x = float(input("x: ").strip())
            y = float(input("y: ").strip())
            z = float(input("z: ").strip())
            spawned = entity_editor.spawn_entity(entity, x, y, z)
            print(f"Spawned entity: {spawned}")
        elif choice == "3":
            entity = armored_zombie()
            world.world_data.setdefault("Level", {}).setdefault("Entities", []).append(entity)
            print(f"Spawned modded mob: {entity}")
        elif choice == "4":
            buy = input("Buy item id: ").strip()
            sell = input("Sell item id: ").strip()
            trade = villager_editor.custom_trade(buy, sell)
            print(f"Added villager trade: {trade}")
        elif choice == "5":
            x = int(input("Chunk x: ").strip())
            z = int(input("Chunk z: ").strip())
            chunk = world.chunk_manager.generate_void_chunk(x, z)
            print(f"Generated chunk: ({chunk['x']}, {chunk['z']})")
        elif choice == "6":
            world.save()
            print("World saved.")
            return
        else:
            print("Invalid option.")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    save_folder = choose_save_folder(args.save_path)
    world = load_world(save_folder)
    interactive_menu(world)


if __name__ == "__main__":
    main()

# ps3-world-editer

CLI-based PS3 Minecraft world editor scaffold for Linux (Python 3.11+).

## Features

- PS3 save-folder detection (`GAMEDATA`, `PARAM.SFO`, `PARAM.PFD`)
- Chunk management (`load`, `save`, `generate_void_chunk`, `delete`, `clone`)
- Inventory editing with illegal/custom items
- Entity spawning/editing, including modded mobs
- Villager trade customization
- Structure and cheat helpers

## Project layout

```
ps3mc_editor/
├── main.py
├── world/
├── editors/
├── cheats/
├── utils/
└── saves/
```

## Quick start

```bash
python -m ps3mc_editor.main
```

On startup, the editor opens a file picker so you can select any file inside a
PS3 save folder. If GUI selection is unavailable, it falls back to a path
prompt in the terminal. Once loaded, use the interactive menu to edit
inventory, entities, villager trades, and chunks, then save.

You can still provide a path directly:

```bash
python -m ps3mc_editor.main --save-path ps3mc_editor/saves/WORLDNAME
```

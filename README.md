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
python -m ps3mc_editor.main --save ps3mc_editor/saves inventory add diamond_sword 64
python -m ps3mc_editor.main --save ps3mc_editor/saves spawn zombie 0 64 0
python -m ps3mc_editor.main --save ps3mc_editor/saves spawn_armored_zombie
python -m ps3mc_editor.main --save ps3mc_editor/saves villager custom_trade dirt diamond
python -m ps3mc_editor.main --save ps3mc_editor/saves chunk generate 0 0
```

Edits are persisted into `world_nbt.json`, chunk binary blobs, and a rebuilt
`GAMEDATA` summary inside the selected save folder.

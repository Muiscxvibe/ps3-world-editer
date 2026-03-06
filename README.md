# PS3 Minecraft World Editor (Linux)

CLI-based editor scaffold for Minecraft: PlayStation 3 Edition saves.

## Features

- PS3 save folder detection and GAMEDATA rebuild using zlib compression.
- Chunk loading, generation, deletion, cloning, and block edits.
- Player/container inventory editing including illegal item stacks.
- Entity spawning/editing and custom villager trade injection.
- Cheat tools for OP items, modded mobs, mob armies, and structure templates.

## Layout

```text
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
python -m ps3mc_editor.main --save ./ps3mc_editor/saves/WORLDNAME inventory add diamond 64
python -m ps3mc_editor.main --save ./ps3mc_editor/saves/WORLDNAME spawn zombie 0 64 0
python -m ps3mc_editor.main --save ./ps3mc_editor/saves/WORLDNAME spawn_armored_zombie
python -m ps3mc_editor.main --save ./ps3mc_editor/saves/WORLDNAME villager custom_trade dirt diamond
python -m ps3mc_editor.main --save ./ps3mc_editor/saves/WORLDNAME chunk generate 0 0
```

## Save folder expectations

A PS3 world save folder should contain at minimum:

- `GAMEDATA`
- `PARAM.SFO`
- `PARAM.PFD`

Optional files like `ICON0.PNG` and `THUMB` are preserved.

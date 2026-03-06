# PS3 Minecraft World Editor (Linux)

A click-based PySide6 desktop tool to open and edit PS3 Minecraft world folders.

## Setup

```bash
pip install PySide6 nbtlib
cd ps3mc_editor
python main.py
```

## Features

- World selector with **Open World**, **Create Void World**, **Recent Worlds**, and **Settings**.
- Tabbed editor for Inventory, Chunks, Entities, Villagers, and Cheats.
- Save pipeline that writes NBT metadata and compressed `GAMEDATA`.
- Linux launcher script (`start_editor.sh`) and desktop entry template.

# PS3 Minecraft World Editor (Linux)

A click-based PySide6 desktop tool to open and edit PS3 Minecraft world folders.

## One-line startup (recommended)

```bash
./ps3mc_editor/start_editor.sh
```

This launcher auto-creates a local virtual environment (`ps3mc_editor/.venv`), installs dependencies, and starts the GUI.

## Optional manual startup

```bash
cd ps3mc_editor
python3 -m venv .venv
. .venv/bin/activate
pip install PySide6 nbtlib
python main.py
```

## Features

- World selector with **Open World**, **Create Void World**, **Recent Worlds**, and **Settings**.
- Tabbed editor for Inventory, Chunks, Entities, Villagers, and Cheats.
- Save pipeline that writes NBT metadata and compressed `GAMEDATA`.
- Linux launcher script (`start_editor.sh`) and desktop entry template.

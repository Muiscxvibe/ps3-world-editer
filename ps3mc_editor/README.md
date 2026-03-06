# PS3 Minecraft World Editor (Linux)

A clickable desktop editor for PS3 Minecraft worlds with world selection, inventory tools, chunk tools, entity spawning at coordinates, villager trade editing, and cheat actions. Supports worlds containing `GAMEDATA` or `GAMEDATA.MS`.

## One-line startup (recommended)

```bash
./ps3mc_editor/start_editor.sh
```

The launcher creates `ps3mc_editor/.venv`, installs dependencies (`PySide6`, `nbtlib`), then starts the GUI.

## What works now

- Startup world selector with:
  - Open World
  - Create Void World
  - Recent Worlds (persisted)
  - Drag-and-drop world folder
- Main editor tabs:
  - Inventory tab with add/remove/edit/illegal item and a live slot grid
  - Chunks tab with load/generate/delete/clone/fill tools
  - Entities tab with spawn/edit/delete plus exact X/Y/Z spawn coordinates
  - Villagers tab with custom trade creation/removal and custom villager spawn
  - Cheats tab with OP sword, item cloud, mob army size control, illegal items
- Save system:
  - Writes compressed `GAMEDATA`
  - Writes `world_state.nbt`

## Troubleshooting

- If the launcher says no display was detected, run it inside a desktop GUI session (not a headless shell).

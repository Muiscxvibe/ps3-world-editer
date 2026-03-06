# ps3-world-editer

PS3 Minecraft World Editor for Linux is available in `ps3mc_editor/`.

## One-line startup

```bash
./ps3mc_editor/start_editor.sh
```

This command sets up a local virtual environment automatically (PEP 668 friendly), installs required dependencies, and starts the GUI.

## Included launcher assets

- Shell launcher: `ps3mc_editor/start_editor.sh`
- Desktop entry template: `ps3mc_editor/ps3mc-editor.desktop`


World detection supports PS3 save folders that contain either `GAMEDATA` or `GAMEDATA.MS` (no hard requirement on `PARAM.SFO`).

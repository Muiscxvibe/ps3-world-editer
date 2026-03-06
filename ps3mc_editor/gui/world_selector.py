from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.ps3world import PS3World
from gui.main_window import MainEditorWindow


class WorldSelectorWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PS3 Minecraft World Editor")
        self.resize(700, 420)

        self.recent_worlds = QListWidget()
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)

        layout.addWidget(QLabel("Select a PlayStation 3 Edition world save directory"))
        layout.addWidget(self.recent_worlds)

        buttons = QHBoxLayout()
        open_btn = QPushButton("Open World")
        open_btn.clicked.connect(self.open_world)

        create_void_btn = QPushButton("Create Void World")
        create_void_btn.clicked.connect(self.create_void_world)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self.show_settings)

        buttons.addWidget(open_btn)
        buttons.addWidget(create_void_btn)
        buttons.addWidget(settings_btn)
        layout.addLayout(buttons)

        self.setCentralWidget(root)

    def open_world(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select PS3 World Folder")
        if not folder:
            return

        world_path = Path(folder)
        world = PS3World(world_path)
        missing = [name for name in ("GAMEDATA", "PARAM.SFO") if not (world_path / name).exists()]
        if missing:
            QMessageBox.warning(
                self,
                "Invalid World",
                f"The selected folder is missing required files: {', '.join(missing)}",
            )
            return

        self.recent_worlds.addItem(str(world_path))
        self._launch_editor(world)

    def create_void_world(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Choose New World Directory")
        if not folder:
            return

        world = PS3World(Path(folder))
        world.create_void_world()
        self.recent_worlds.addItem(str(world.path))
        self._launch_editor(world)

    def show_settings(self) -> None:
        QMessageBox.information(self, "Settings", "Settings will be added in a future update.")

    def _launch_editor(self, world: PS3World) -> None:
        editor = MainEditorWindow(world)
        editor.show()
        self.close()
        self._editor = editor

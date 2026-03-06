from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtGui import QDragEnterEvent, QDropEvent
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
        self.resize(760, 460)
        self.setAcceptDrops(True)
        self.recent_file = Path.home() / ".ps3mc_editor_recent.json"

        self.recent_worlds = QListWidget()
        self._build_ui()
        self._load_recent_worlds()

    def _build_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)

        layout.addWidget(QLabel("Select or drag-and-drop a PlayStation 3 Edition world save directory."))
        layout.addWidget(self.recent_worlds)
        self.recent_worlds.itemDoubleClicked.connect(lambda item: self.open_world(Path(item.text())))

        buttons = QHBoxLayout()
        open_btn = QPushButton("Open World")
        open_btn.clicked.connect(lambda: self.open_world())

        create_void_btn = QPushButton("Create Void World")
        create_void_btn.clicked.connect(self.create_void_world)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self.show_settings)

        buttons.addWidget(open_btn)
        buttons.addWidget(create_void_btn)
        buttons.addWidget(settings_btn)
        layout.addLayout(buttons)

        self.setCentralWidget(root)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:  # noqa: N802
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:  # noqa: N802
        urls = event.mimeData().urls()
        if not urls:
            return
        path = Path(urls[0].toLocalFile())
        if path.is_dir():
            self.open_world(path)

    def _load_recent_worlds(self) -> None:
        if not self.recent_file.exists():
            return
        try:
            worlds = json.loads(self.recent_file.read_text(encoding="utf-8"))
            for world in worlds:
                if Path(world).exists():
                    self.recent_worlds.addItem(world)
        except (json.JSONDecodeError, OSError):
            return

    def _save_recent_worlds(self) -> None:
        paths = [self.recent_worlds.item(i).text() for i in range(self.recent_worlds.count())]
        self.recent_file.write_text(json.dumps(paths[:10], indent=2), encoding="utf-8")

    def open_world(self, selected: Path | None = None) -> None:
        world_path = selected
        if world_path is None:
            folder = QFileDialog.getExistingDirectory(self, "Select PS3 World Folder")
            if not folder:
                return
            world_path = Path(folder)

        world = PS3World(world_path)
        if not world.is_world_folder():
            QMessageBox.warning(
                self,
                "Invalid World",
                "The selected folder is missing a PS3 world data file. Expected one of: "
                "GAMEDATA or GAMEDATA.MS",
            )
            return

        world.load()
        self._remember_world(world_path)
        self._launch_editor(world)

    def _remember_world(self, world_path: Path) -> None:
        as_str = str(world_path)
        current = [self.recent_worlds.item(i).text() for i in range(self.recent_worlds.count())]
        if as_str in current:
            current.remove(as_str)
        current.insert(0, as_str)
        self.recent_worlds.clear()
        self.recent_worlds.addItems(current[:10])
        self._save_recent_worlds()

    def create_void_world(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Choose New World Directory")
        if not folder:
            return

        world = PS3World(Path(folder))
        world.create_void_world()
        self._remember_world(world.path)
        self._launch_editor(world)

    def show_settings(self) -> None:
        QMessageBox.information(
            self,
            "Settings",
            "Settings are minimal for now.\nTip: double-click recent worlds or drag-and-drop folders.",
        )

    def _launch_editor(self, world: PS3World) -> None:
        editor = MainEditorWindow(world)
        editor.show()
        self.close()
        self._editor = editor

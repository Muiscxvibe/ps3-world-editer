from __future__ import annotations

from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QToolBar,
)

from core.ps3world import PS3World
from gui.cheat_panel import CheatPanel
from gui.chunk_manager_window import ChunkManagerWindow
from gui.entity_editor_window import EntityEditorWindow
from gui.inventory_window import InventoryWindow
from gui.villager_editor_window import VillagerEditorWindow


class MainEditorWindow(QMainWindow):
    def __init__(self, world: PS3World) -> None:
        super().__init__()
        self.world = world

        self.setWindowTitle(f"PS3 World Editor - {world.path.name}")
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        self.tabs.addTab(InventoryWindow(world), "Inventory")
        self.tabs.addTab(ChunkManagerWindow(world), "Chunks")
        self.tabs.addTab(EntityEditorWindow(world), "Entities")
        self.tabs.addTab(VillagerEditorWindow(world), "Villagers")
        self.tabs.addTab(CheatPanel(world), "Cheats")

        self.setCentralWidget(self.tabs)
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("World loaded")

        save_toolbar = QToolBar("Save")
        save_btn = QPushButton("Save World")
        save_btn.clicked.connect(self.save_world)
        save_toolbar.addWidget(save_btn)
        self.addToolBar(save_toolbar)

    def save_world(self) -> None:
        self.world.save()
        self.statusBar().showMessage("World saved successfully")
        QMessageBox.information(self, "Save", "World saved successfully")

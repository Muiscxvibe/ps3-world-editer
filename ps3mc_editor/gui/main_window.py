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
        self.resize(1100, 760)

        self.inventory_tab = InventoryWindow(world)
        self.chunk_tab = ChunkManagerWindow(world)
        self.entity_tab = EntityEditorWindow(world)
        self.villager_tab = VillagerEditorWindow(world)
        self.cheat_tab = CheatPanel(world)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.inventory_tab, "Inventory")
        self.tabs.addTab(self.chunk_tab, "Chunks")
        self.tabs.addTab(self.entity_tab, "Entities")
        self.tabs.addTab(self.villager_tab, "Villagers")
        self.tabs.addTab(self.cheat_tab, "Cheats")

        self.setCentralWidget(self.tabs)
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("World loaded")

        save_toolbar = QToolBar("Save")
        save_btn = QPushButton("Save World")
        save_btn.clicked.connect(self.save_world)
        refresh_btn = QPushButton("Refresh Tabs")
        refresh_btn.clicked.connect(self.refresh_views)
        save_toolbar.addWidget(save_btn)
        save_toolbar.addWidget(refresh_btn)
        self.addToolBar(save_toolbar)

    def refresh_views(self) -> None:
        self.inventory_tab.refresh_grid()
        self.entity_tab.refresh_list()
        self.villager_tab.refresh_list()
        self.statusBar().showMessage("Views refreshed", 3000)

    def save_world(self) -> None:
        self.world.save()
        self.statusBar().showMessage("World saved successfully")
        QMessageBox.information(self, "Save", "World saved successfully")

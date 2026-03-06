from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.ps3world import PS3World


class EntityEditorWindow(QWidget):
    def __init__(self, world: PS3World) -> None:
        super().__init__()
        self.world = world
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        self.entities = QListWidget()
        root.addWidget(self.entities)
        self.refresh_list()

        controls = QHBoxLayout()
        self.mob_selector = QComboBox()
        self.mob_selector.addItems(["Zombie", "Skeleton", "Creeper", "Villager", "Enderman"])

        spawn_btn = QPushButton("Spawn Mob")
        spawn_btn.clicked.connect(self.spawn_mob)
        delete_btn = QPushButton("Delete Mob")
        delete_btn.clicked.connect(self.delete_mob)
        edit_btn = QPushButton("Edit Mob")
        edit_btn.clicked.connect(self.edit_mob)

        armored_btn = QPushButton("Spawn Armored Zombie")
        armored_btn.clicked.connect(self.armored_zombie)
        giant_btn = QPushButton("Spawn Giant Mob")
        giant_btn.clicked.connect(self.giant_mob)
        speed_btn = QPushButton("Spawn Speed Mob")
        speed_btn.clicked.connect(self.speed_mob)
        invisible_btn = QPushButton("Spawn Invisible Mob")
        invisible_btn.clicked.connect(self.invisible_mob)

        for widget in [
            self.mob_selector,
            spawn_btn,
            delete_btn,
            edit_btn,
            armored_btn,
            giant_btn,
            speed_btn,
            invisible_btn,
        ]:
            controls.addWidget(widget)
        root.addLayout(controls)

    def refresh_list(self) -> None:
        self.entities.clear()
        for entity in self.world.entities.list_entities():
            self.entities.addItem(f"{entity['id']} ({entity['x']},{entity['y']},{entity['z']})")

    def spawn_mob(self) -> None:
        self.world.entities.spawn(self.mob_selector.currentText())
        self.refresh_list()

    def delete_mob(self) -> None:
        row = self.entities.currentRow()
        if row >= 0:
            self.world.entities.delete(row)
            self.refresh_list()

    def edit_mob(self) -> None:
        row = self.entities.currentRow()
        if row >= 0:
            self.world.entities.edit(row, {"Health": 40.0})
            self.refresh_list()

    def armored_zombie(self) -> None:
        self.world.entities.spawn_armored_zombie()
        self.refresh_list()

    def giant_mob(self) -> None:
        self.world.entities.spawn_giant_mob()
        self.refresh_list()

    def speed_mob(self) -> None:
        self.world.entities.spawn_speed_mob()
        self.refresh_list()

    def invisible_mob(self) -> None:
        self.world.entities.spawn_invisible_mob()
        self.refresh_list()

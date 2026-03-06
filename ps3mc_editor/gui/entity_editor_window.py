from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QListWidget,
    QMessageBox,
    QPushButton,
    QSpinBox,
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

        form = QFormLayout()
        self.mob_selector = QComboBox()
        self.mob_selector.addItems(["Zombie", "Skeleton", "Creeper", "Villager", "Enderman"])
        self.x = QSpinBox()
        self.y = QSpinBox()
        self.z = QSpinBox()
        for spin in [self.x, self.y, self.z]:
            spin.setRange(-30000, 30000)
        self.y.setValue(64)

        form.addRow("Mob", self.mob_selector)
        form.addRow("X", self.x)
        form.addRow("Y", self.y)
        form.addRow("Z", self.z)
        root.addLayout(form)

        controls = QHBoxLayout()
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

    def _xyz(self) -> tuple[int, int, int]:
        return self.x.value(), self.y.value(), self.z.value()

    def spawn_mob(self) -> None:
        x, y, z = self._xyz()
        self.world.entities.spawn(self.mob_selector.currentText(), x=x, y=y, z=z)
        self.refresh_list()

    def delete_mob(self) -> None:
        row = self.entities.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Entity Editor", "Select an entity to delete.")
            return
        self.world.entities.delete(row)
        self.refresh_list()

    def edit_mob(self) -> None:
        row = self.entities.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Entity Editor", "Select an entity to edit.")
            return
        self.world.entities.edit(row, {"x": self.x.value(), "y": self.y.value(), "z": self.z.value(), "Health": 40.0})
        self.refresh_list()

    def armored_zombie(self) -> None:
        x, y, z = self._xyz()
        self.world.entities.spawn_armored_zombie(x=x, y=y, z=z)
        self.refresh_list()

    def giant_mob(self) -> None:
        x, y, z = self._xyz()
        self.world.entities.spawn_giant_mob(self.mob_selector.currentText(), x=x, y=y, z=z)
        self.refresh_list()

    def speed_mob(self) -> None:
        x, y, z = self._xyz()
        self.world.entities.spawn_speed_mob(self.mob_selector.currentText(), x=x, y=y, z=z)
        self.refresh_list()

    def invisible_mob(self) -> None:
        x, y, z = self._xyz()
        self.world.entities.spawn_invisible_mob(self.mob_selector.currentText(), x=x, y=y, z=z)
        self.refresh_list()

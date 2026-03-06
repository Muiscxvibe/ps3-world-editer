from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from core.ps3world import PS3World


class InventoryWindow(QWidget):
    def __init__(self, world: PS3World) -> None:
        super().__init__()
        self.world = world
        self.slots: list[QLabel] = []
        self._build_ui()
        self.refresh_grid()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.addWidget(QLabel("Inventory Grid"))

        grid = QGridLayout()
        for i in range(4):
            for j in range(9):
                slot = QLabel("[empty]")
                slot.setStyleSheet("border: 1px solid gray; padding: 6px;")
                grid.addWidget(slot, i, j)
                self.slots.append(slot)
        root.addLayout(grid)

        controls = QHBoxLayout()
        self.item_selector = QComboBox()
        self.item_selector.setEditable(True)
        self.item_selector.addItems([
            "diamond",
            "diamond_sword",
            "spawn_egg",
            "enchanted_book",
            "golden_apple",
        ])

        self.count = QSpinBox()
        self.count.setRange(1, 64)
        self.count.setValue(1)

        add_btn = QPushButton("Add Item")
        add_btn.clicked.connect(self.add_item)
        remove_btn = QPushButton("Remove Item")
        remove_btn.clicked.connect(self.remove_item)
        edit_btn = QPushButton("Edit Item")
        edit_btn.clicked.connect(self.edit_item)
        illegal_btn = QPushButton("Spawn Illegal Item")
        illegal_btn.clicked.connect(self.spawn_illegal)

        controls.addWidget(self.item_selector)
        controls.addWidget(self.count)
        controls.addWidget(add_btn)
        controls.addWidget(remove_btn)
        controls.addWidget(edit_btn)
        controls.addWidget(illegal_btn)
        root.addLayout(controls)

    def refresh_grid(self) -> None:
        for label, slot in zip(self.slots, self.world.inventory.as_slots(), strict=False):
            if slot is None:
                label.setText("[empty]")
            else:
                label.setText(f"{slot.item_id}\nx{slot.count}")

    def _current_item(self) -> str:
        return self.item_selector.currentText().strip()

    def add_item(self) -> None:
        item = self._current_item()
        if not item:
            QMessageBox.warning(self, "Inventory", "Item id cannot be empty.")
            return
        self.world.inventory.add_item(item, self.count.value())
        self.refresh_grid()

    def remove_item(self) -> None:
        item = self._current_item()
        self.world.inventory.remove_item(item)
        self.refresh_grid()

    def edit_item(self) -> None:
        item = self._current_item()
        if not item:
            return
        self.world.inventory.edit_item(item, self.count.value())
        self.refresh_grid()

    def spawn_illegal(self) -> None:
        item = self._current_item()
        self.world.inventory.spawn_illegal_item(item)
        self.refresh_grid()

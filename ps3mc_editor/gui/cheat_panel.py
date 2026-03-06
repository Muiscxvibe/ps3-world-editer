from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from core.ps3world import PS3World


class CheatPanel(QWidget):
    def __init__(self, world: PS3World) -> None:
        super().__init__()
        self.world = world
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        row = QHBoxLayout()

        op_sword = QPushButton("Give OP Sword")
        op_sword.setToolTip("Sharpness 1000 + Knockback 50")
        op_sword.clicked.connect(self.world.inventory.give_op_sword)

        cloud = QPushButton("Spawn Item Cloud")
        cloud.clicked.connect(self.world.cheats.spawn_item_cloud)

        army = QPushButton("Spawn Mob Army")
        army.clicked.connect(lambda: self.world.cheats.spawn_mob_army("Zombie", 100))

        illegal = QPushButton("Give Illegal Items")
        illegal.clicked.connect(self.world.cheats.give_illegal_items)

        for btn in [op_sword, cloud, army, illegal]:
            row.addWidget(btn)

        root.addLayout(row)

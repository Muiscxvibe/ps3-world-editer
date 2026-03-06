from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from core.ps3world import PS3World


class VillagerEditorWindow(QWidget):
    def __init__(self, world: PS3World) -> None:
        super().__init__()
        self.world = world
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        self.villagers = QListWidget()
        root.addWidget(self.villagers)
        self.refresh_list()

        trade_panel = QHBoxLayout()
        self.buy_count = QSpinBox()
        self.buy_count.setRange(1, 64)
        self.buy_count.setValue(1)

        self.sell_count = QSpinBox()
        self.sell_count.setRange(1, 64)
        self.sell_count.setValue(64)

        self.uses = QSpinBox()
        self.uses.setRange(0, 999)
        self.max_uses = QSpinBox()
        self.max_uses.setRange(1, 999)
        self.max_uses.setValue(999)

        add_trade = QPushButton("Add Trade")
        add_trade.clicked.connect(self.add_trade)
        remove_trade = QPushButton("Remove Trade")
        remove_trade.clicked.connect(self.remove_trade)
        create_custom = QPushButton("Create Custom Villager")
        create_custom.clicked.connect(self.create_custom_villager)

        for widget in [
            self.buy_count,
            self.sell_count,
            self.uses,
            self.max_uses,
            add_trade,
            remove_trade,
            create_custom,
        ]:
            trade_panel.addWidget(widget)
        root.addLayout(trade_panel)

    def refresh_list(self) -> None:
        self.villagers.clear()
        for villager in self.world.entities.list_villagers():
            self.villagers.addItem(villager["id"])

    def add_trade(self) -> None:
        trade = {
            "buy": {"id": "minecraft:dirt", "Count": self.buy_count.value()},
            "sell": {"id": "minecraft:diamond", "Count": self.sell_count.value()},
            "uses": self.uses.value(),
            "maxUses": self.max_uses.value(),
        }
        self.world.entities.add_trade_to_selected_villager(trade)

    def remove_trade(self) -> None:
        self.world.entities.remove_trade_from_selected_villager()

    def create_custom_villager(self) -> None:
        self.world.entities.create_custom_villager()
        self.refresh_list()

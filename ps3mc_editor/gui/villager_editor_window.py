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

        trade_form = QFormLayout()
        self.buy_item = QComboBox()
        self.buy_item.setEditable(True)
        self.buy_item.addItems(["minecraft:dirt", "minecraft:emerald", "minecraft:diamond"])
        self.sell_item = QComboBox()
        self.sell_item.setEditable(True)
        self.sell_item.addItems(["minecraft:diamond", "minecraft:enchanted_book", "minecraft:gold_ingot"])

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

        trade_form.addRow("Buy Item", self.buy_item)
        trade_form.addRow("Buy Count", self.buy_count)
        trade_form.addRow("Sell Item", self.sell_item)
        trade_form.addRow("Sell Count", self.sell_count)
        trade_form.addRow("Uses", self.uses)
        trade_form.addRow("Max Uses", self.max_uses)
        root.addLayout(trade_form)

        trade_panel = QHBoxLayout()
        add_trade = QPushButton("Add Trade")
        add_trade.clicked.connect(self.add_trade)
        remove_trade = QPushButton("Remove Trade")
        remove_trade.clicked.connect(self.remove_trade)
        create_custom = QPushButton("Create Custom Villager")
        create_custom.clicked.connect(self.create_custom_villager)

        for widget in [add_trade, remove_trade, create_custom]:
            trade_panel.addWidget(widget)
        root.addLayout(trade_panel)

    def refresh_list(self) -> None:
        self.villagers.clear()
        for idx, villager in enumerate(self.world.entities.list_villagers()):
            trade_count = len(villager.get("Trades", []))
            self.villagers.addItem(f"Villager #{idx} ({villager['x']},{villager['y']},{villager['z']}) - trades: {trade_count}")

    def _selected_villager(self) -> int:
        return max(self.villagers.currentRow(), 0)

    def add_trade(self) -> None:
        trade = {
            "buy": {"id": self.buy_item.currentText().strip(), "Count": self.buy_count.value()},
            "sell": {"id": self.sell_item.currentText().strip(), "Count": self.sell_count.value()},
            "uses": self.uses.value(),
            "maxUses": self.max_uses.value(),
        }
        success = self.world.entities.add_trade_to_villager(self._selected_villager(), trade)
        if not success:
            QMessageBox.warning(self, "Villager Editor", "No villager available. Create one first.")
        self.refresh_list()

    def remove_trade(self) -> None:
        success = self.world.entities.remove_trade_from_villager(self._selected_villager())
        if not success:
            QMessageBox.warning(self, "Villager Editor", "Selected villager has no trades.")
        self.refresh_list()

    def create_custom_villager(self) -> None:
        self.world.entities.create_custom_villager()
        self.refresh_list()

import sys

from PySide6.QtWidgets import QApplication

from gui.world_selector import WorldSelectorWindow


def run() -> None:
    app = QApplication(sys.argv)
    window = WorldSelectorWindow()
    window.show()
    sys.exit(app.exec())

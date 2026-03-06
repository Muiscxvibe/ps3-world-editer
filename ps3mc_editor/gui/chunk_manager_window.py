from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.ps3world import PS3World


class ChunkManagerWindow(QWidget):
    def __init__(self, world: PS3World) -> None:
        super().__init__()
        self.world = world
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        coords = QHBoxLayout()
        self.chunk_x = QLineEdit("0")
        self.chunk_z = QLineEdit("0")
        coords.addWidget(QLabel("Chunk X"))
        coords.addWidget(self.chunk_x)
        coords.addWidget(QLabel("Chunk Z"))
        coords.addWidget(self.chunk_z)
        root.addLayout(coords)

        buttons = QHBoxLayout()
        actions = [
            ("Load Chunk", self.load_chunk),
            ("Generate Void Chunk", self.void_chunk),
            ("Delete Chunk", self.delete_chunk),
            ("Clone Chunk", self.clone_chunk),
            ("Fill Chunk With Block", self.fill_chunk),
        ]

        for text, handler in actions:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            buttons.addWidget(btn)

        root.addLayout(buttons)

    def _coords(self) -> tuple[int, int]:
        return int(self.chunk_x.text()), int(self.chunk_z.text())

    def load_chunk(self) -> None:
        self.world.chunks.load_chunk(*self._coords())

    def void_chunk(self) -> None:
        self.world.chunks.generate_void_chunk(*self._coords())

    def delete_chunk(self) -> None:
        self.world.chunks.delete_chunk(*self._coords())

    def clone_chunk(self) -> None:
        x, z = self._coords()
        self.world.chunks.clone_chunk(x, z, x + 1, z + 1)

    def fill_chunk(self) -> None:
        self.world.chunks.fill_chunk(*self._coords(), block="diamond_block")

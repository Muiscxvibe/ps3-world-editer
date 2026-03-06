from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
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
        self.fill_block = QLineEdit("diamond_block")
        coords.addWidget(QLabel("Chunk X"))
        coords.addWidget(self.chunk_x)
        coords.addWidget(QLabel("Chunk Z"))
        coords.addWidget(self.chunk_z)
        coords.addWidget(QLabel("Fill Block"))
        coords.addWidget(self.fill_block)
        root.addLayout(coords)

        buttons = QHBoxLayout()
        actions = [
            ("Load Chunk", self.load_chunk),
            ("Generate Void Chunk", self.void_chunk),
            ("Delete Chunk", self.delete_chunk),
            ("Clone Chunk -> +1,+1", self.clone_chunk),
            ("Fill Chunk With Block", self.fill_chunk),
        ]

        for text, handler in actions:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            buttons.addWidget(btn)

        root.addLayout(buttons)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        root.addWidget(self.output)

    def _coords(self) -> tuple[int, int] | None:
        try:
            return int(self.chunk_x.text()), int(self.chunk_z.text())
        except ValueError:
            QMessageBox.warning(self, "Chunk Manager", "Chunk coordinates must be integers.")
            return None

    def load_chunk(self) -> None:
        coords = self._coords()
        if coords is None:
            return
        chunk = self.world.chunks.load_chunk(*coords)
        self.output.setPlainText(str(chunk))

    def void_chunk(self) -> None:
        coords = self._coords()
        if coords is None:
            return
        self.world.chunks.generate_void_chunk(*coords)
        self.load_chunk()

    def delete_chunk(self) -> None:
        coords = self._coords()
        if coords is None:
            return
        self.world.chunks.delete_chunk(*coords)
        self.output.setPlainText(f"Deleted chunk {coords}")

    def clone_chunk(self) -> None:
        coords = self._coords()
        if coords is None:
            return
        x, z = coords
        self.world.chunks.clone_chunk(x, z, x + 1, z + 1)
        self.output.setPlainText(f"Cloned chunk {(x, z)} -> {(x + 1, z + 1)}")

    def fill_chunk(self) -> None:
        coords = self._coords()
        if coords is None:
            return
        block = self.fill_block.text().strip() or "diamond_block"
        self.world.chunks.fill_chunk(*coords, block=block)
        self.load_chunk()

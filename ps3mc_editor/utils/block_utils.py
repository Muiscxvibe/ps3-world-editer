"""Utilities for chunk-local block coordinates and palettes."""

from __future__ import annotations

from dataclasses import dataclass

CHUNK_WIDTH = 16
CHUNK_DEPTH = 16
CHUNK_HEIGHT = 128


@dataclass(slots=True)
class BlockPosition:
    x: int
    y: int
    z: int

    def validate(self) -> None:
        if not (0 <= self.x < CHUNK_WIDTH):
            raise ValueError(f"x out of bounds: {self.x}")
        if not (0 <= self.z < CHUNK_DEPTH):
            raise ValueError(f"z out of bounds: {self.z}")
        if not (0 <= self.y < CHUNK_HEIGHT):
            raise ValueError(f"y out of bounds: {self.y}")


def create_empty_chunk(fill: str = "air") -> list[list[list[str]]]:
    """Create a 16x16x128 chunk filled with one block id."""
    return [[[fill for _ in range(CHUNK_HEIGHT)] for _ in range(CHUNK_DEPTH)] for _ in range(CHUNK_WIDTH)]

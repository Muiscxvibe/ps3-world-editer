"""Block and chunk-space helpers."""

from __future__ import annotations

CHUNK_WIDTH = 16
CHUNK_LENGTH = 16
CHUNK_HEIGHT = 128


def in_chunk_bounds(x: int, y: int, z: int) -> bool:
    """True when local block coordinates are valid for PS3 chunk dimensions."""
    return 0 <= x < CHUNK_WIDTH and 0 <= z < CHUNK_LENGTH and 0 <= y < CHUNK_HEIGHT


def chunk_key(x: int, z: int) -> str:
    """Stable chunk key used in dictionaries and JSON payloads."""
    return f"{x},{z}"

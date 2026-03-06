"""Compression helpers for PS3 Minecraft chunk payloads."""

from __future__ import annotations

import zlib


def compress_payload(data: bytes, level: int = 9) -> bytes:
    """Compress a payload with zlib using a default high compression level."""
    return zlib.compress(data, level=level)


def decompress_payload(data: bytes) -> bytes:
    """Decompress a zlib payload."""
    return zlib.decompress(data)

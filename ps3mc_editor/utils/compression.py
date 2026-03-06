"""Compression helpers used when rebuilding PS3 chunk payloads."""

from __future__ import annotations

import zlib


def compress_payload(payload: bytes, level: int = 9) -> bytes:
    """Compress raw chunk/game data using zlib."""
    return zlib.compress(payload, level)


def decompress_payload(payload: bytes) -> bytes:
    """Decompress zlib-compressed payload."""
    return zlib.decompress(payload)

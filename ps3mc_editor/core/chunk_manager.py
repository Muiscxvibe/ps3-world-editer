from __future__ import annotations


class ChunkManager:
    def __init__(self) -> None:
        self.chunks: dict[tuple[int, int], dict] = {}

    def to_dict(self) -> dict[str, dict]:
        return {f"{x},{z}": payload for (x, z), payload in self.chunks.items()}

    def load_dict(self, data: dict[str, dict]) -> None:
        chunks: dict[tuple[int, int], dict] = {}
        for key, payload in data.items():
            x_str, z_str = key.split(",", 1)
            chunks[(int(x_str), int(z_str))] = payload
        self.chunks = chunks

    def load_chunk(self, x: int, z: int) -> dict:
        return self.chunks.get((x, z), {"x": x, "z": z, "status": "empty", "blocks": []})

    def generate_void_chunk(self, x: int, z: int) -> None:
        self.chunks[(x, z)] = {"x": x, "z": z, "blocks": [], "status": "void"}

    def delete_chunk(self, x: int, z: int) -> None:
        self.chunks.pop((x, z), None)

    def clone_chunk(self, src_x: int, src_z: int, dst_x: int, dst_z: int) -> None:
        source = self.chunks.get((src_x, src_z), {"x": src_x, "z": src_z, "blocks": [], "status": "empty"})
        self.chunks[(dst_x, dst_z)] = {**source, "x": dst_x, "z": dst_z}

    def fill_chunk(self, x: int, z: int, block: str) -> None:
        self.chunks[(x, z)] = {
            "x": x,
            "z": z,
            "status": "filled",
            "blocks": [block] * (16 * 16),
            "block": block,
        }

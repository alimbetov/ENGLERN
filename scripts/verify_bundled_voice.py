"""Validate the exact user-supplied Lessac pair before packaging."""
import hashlib
import json
import sys
from pathlib import Path

EXPECTED = {
    "en_US-lessac-high.onnx": "4cabf7c3a638017137f34a1516522032d4fe3f38228a843cc9b764ddcbcd9e09",
    "en_US-lessac-high.onnx.json": "8f854da3d71a346943850224886d0baa5f36a10e5cdf735bcd8d3cf582a6539a",
}

def verify(directory: Path) -> None:
    for name, expected in EXPECTED.items():
        with (directory / name).open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != expected:
            raise ValueError(f"Voice hash mismatch: {name}")
    config = json.loads((directory / "en_US-lessac-high.onnx.json").read_text(encoding="utf-8"))
    if config["audio"]["sample_rate"] != 22050 or config["language"]["code"] != "en_US":
        raise ValueError("Unexpected voice configuration")
    print("Bundled voice integrity PASS")

if __name__ == "__main__":
    verify(Path(sys.argv[1]))

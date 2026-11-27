"""Pinned LJ Speech qualification fixture; config uses upstream size/MD5 pending SHA256 freeze."""
import hashlib
import json
import sys
from pathlib import Path
from urllib.request import urlopen

BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/217ddc79818708b078d0d14a8fae9608b9d77141/en/en_US/ljspeech/high/"
FILES = {
    "en_US-ljspeech-high.onnx": (114199011, "dad093b5d2cff6a5fda99883ceda09d1", "5d4f08ba6a2a48c44592eed3ce56bf85e9de3dd4e20df90541ae68a8310c029a"),
    "en_US-ljspeech-high.onnx.json": (4970, "de98fc398ddead60fb82d93bfafb3ad1", None),
    "MODEL_CARD": (515, "59322a9a8d2c0e556f0be1171cd54ea7", None),
}

def verify(directory: Path) -> None:
    evidence = {}
    for name, (size, md5, sha) in FILES.items():
        path = directory / name
        if path.stat().st_size != size:
            raise ValueError(f"Size mismatch: {name}")
        with path.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        with path.open("rb") as stream:
            legacy = hashlib.file_digest(stream, "md5").hexdigest()
        if legacy != md5 or (sha is not None and actual != sha):
            raise ValueError(f"Digest mismatch: {name}")
        evidence[name] = {"sizeBytes": size, "sha256": actual}
    config = json.loads((directory / "en_US-ljspeech-high.onnx.json").read_text(encoding="utf-8"))
    if config["audio"]["sample_rate"] != 22050 or config["language"]["code"] != "en_US":
        raise ValueError("Unexpected voice configuration")
    (directory / "VOICE-EVIDENCE.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    (directory / "VOICE-NOTICE.txt").write_text("LJ Speech High: model author declares public domain. https://brycebeattie.com/files/tts/\nDataset: https://keithito.com/LJ-Speech-Dataset/\nSource revision: 217ddc79818708b078d0d14a8fae9608b9d77141\nRepository metadata: MIT. Internal qualification only; distribution admission separate.\n", encoding="utf-8")
    print(json.dumps(evidence))

def download(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=False)
    for name, (size, _, _) in FILES.items():
        with urlopen(BASE + name, timeout=120) as response, (directory / name).open("xb") as output:
            remaining = size
            while remaining:
                chunk = response.read(min(1024 * 1024, remaining))
                if not chunk:
                    raise ValueError(f"Truncated file: {name}")
                output.write(chunk)
                remaining -= len(chunk)
            if response.read(1):
                raise ValueError(f"Oversized file: {name}")
    verify(directory)

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--download":
        download(Path(sys.argv[2]))
    else:
        verify(Path(sys.argv[1]))

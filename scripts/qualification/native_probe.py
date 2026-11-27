"""Independent runtime probe, no application source or voice models."""
import hashlib
import json
import os
import platform
import re
import sqlite3
import sys
import tomllib
from importlib.metadata import distributions, version
from pathlib import Path

import numpy as np
import onnxruntime as ort
from PySide6 import QtCore, QtMultimedia
from piper import PiperVoice

def varint(n):
    result = bytearray()
    while n > 127:
        result.append((n & 127) | 128)
        n >>= 7
    result.append(n)
    return bytes(result)

def integer(field, n):
    return varint(field << 3) + varint(n)

def field(field_id, value):
    return varint((field_id << 3) | 2) + varint(len(value)) + value

def tensor(name):
    shape = field(1, integer(1, 2))
    tensor_type = integer(1, 1) + field(2, shape)
    return field(1, name) + field(2, field(1, tensor_type))

def model():
    # ONNX IR 8, opset 13: float32 Y = X + X, shape [2].
    node = field(1, b"X") + field(1, b"X") + field(2, b"Y") + field(4, b"Add")
    graph = field(1, node) + field(2, b"add") + field(11, tensor(b"X")) + field(12, tensor(b"Y"))
    return integer(1, 8) + field(7, graph) + field(8, integer(2, 13))

def main():
    out = Path("evidence")
    out.mkdir(exist_ok=True)
    lock = Path("uv.lock").read_bytes()
    assert hashlib.sha256(lock).hexdigest() == "c68e7e8cb941f0f21892f27f2b7ab03e619b0f19763cbe8478eb4195643e3c98"
    assert sys.version_info[:3] == (3, 12, 16)
    target = (sys.platform, platform.machine().lower())
    assert target == (("win32", "amd64") if os.environ["RUNNER_OS"] == "Windows" else ("darwin", "arm64"))
    pins = {p["name"]: p["version"] for p in tomllib.loads(lock.decode())["package"] if "registry" in p.get("source", {})}
    for name in ("pyside6", "pyside6-addons", "pyside6-essentials", "shiboken6"):
        assert version(name) == pins[name] == "6.11.1"
    assert QtCore.qVersion() == "6.11.1"
    assert callable(PiperVoice.load) and callable(PiperVoice.synthesize_wav)
    assert "CPUExecutionProvider" in ort.get_available_providers()
    session = ort.InferenceSession(model(), providers=["CPUExecutionProvider"])
    result = session.run(["Y"], {"X": np.array([1.25, -3], dtype=np.float32)})[0]
    np.testing.assert_array_equal(result, np.array([2.5, -6], dtype=np.float32))
    with sqlite3.connect(":memory:") as db:
        db.execute("PRAGMA foreign_keys=ON")
        assert db.execute("PRAGMA foreign_keys").fetchone() == (1,)
    inventory = []
    for d in distributions():
        name = re.sub(r"[-_.]+", "-", d.metadata["Name"]).lower()
        assert name in pins and pins[name] == d.version, f"unexpected distribution {name}=={d.version}"
        inventory.append({"name": name, "version": d.version, "license_expression": d.metadata.get("License-Expression"), "license": d.metadata.get("License"), "license_classifiers": [x for x in d.metadata.get_all("Classifier", []) if x.startswith("License ::")], "license_files": d.metadata.get_all("License-File", [])})
    inventory.sort(key=lambda x: x["name"])
    assert {"numpy", "onnxruntime", "piper-tts", "pyside6", "pyinstaller", "pytest", "ruff"} <= {x["name"] for x in inventory}
    (out / "installed.txt").write_text("".join(f"{d['name']}=={d['version']}\n" for d in inventory), encoding="utf-8")
    (out / "licenses.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    (out / "native.json").write_text(json.dumps({"sha": os.environ["GITHUB_SHA"], "lock_sha256": hashlib.sha256(lock).hexdigest(), "platform": list(target), "python": platform.python_version(), "qt": QtCore.qVersion(), "onnxruntime": ort.__version__, "numpy": np.__version__, "onnx_inference": "PASS", "piper_api": "PASS", "piper_synthesis": "NOT_RUN"}, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()

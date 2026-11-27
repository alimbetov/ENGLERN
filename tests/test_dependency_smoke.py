import importlib.metadata as md
import platform
import sqlite3
import sys


def test_target_runtime():
    assert sys.version_info[:3] == (3, 12, 16)
    assert (platform.system(), platform.machine().lower()) in {
        ("Windows", "amd64"), ("Windows", "x86_64"), ("Darwin", "arm64")
    }


def test_qt_alignment(qapp):
    from PySide6 import QtCore, QtMultimedia
    for package in ("PySide6", "PySide6-Essentials", "PySide6-Addons", "shiboken6"):
        assert md.version(package) == "6.11.1"
    assert QtCore.qVersion() == "6.11.1"
    assert QtMultimedia.QMediaPlayer() is not None


def test_native_numeric_runtime():
    import numpy as np
    import onnxruntime as ort
    assert np.array([1, 2], dtype=np.float32).sum() == 3
    assert "CPUExecutionProvider" in ort.get_available_providers()


def test_piper_api():
    from piper import PiperVoice
    assert md.version("piper-tts") == "1.4.2"
    assert callable(PiperVoice.load)
    assert callable(PiperVoice.synthesize_wav)


def test_sqlite():
    with sqlite3.connect(":memory:") as conn:
        conn.execute("PRAGMA foreign_keys=ON")
        assert conn.execute("PRAGMA foreign_keys").fetchone() == (1,)


def test_packaging_import():
    import PyInstaller
    assert PyInstaller.__version__ == "6.21.0"

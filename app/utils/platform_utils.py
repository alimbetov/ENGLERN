from pathlib import Path
import os
import sys


def app_root() -> Path:
    if getattr(sys, "frozen", False):
        if sys.platform == "darwin":
            return Path.home() / "Library" / "Application Support" / "ENGLERN"
        if sys.platform == "win32":
            return Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "ENGLERN"
        return Path.home() / ".local" / "share" / "ENGLERN"
    return Path(__file__).resolve().parents[2]


def _directory(name: str) -> Path:
    path = app_root() / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def voices_dir() -> Path:
    return _directory("voices")


def audio_dir() -> Path:
    return _directory("audio")


def texts_dir() -> Path:
    return _directory("texts")

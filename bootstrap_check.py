import platform
import sys
from pathlib import Path


def check_python() -> None:
    print("Python:", sys.version)
    print("Executable:", sys.executable)
    print("Platform:", platform.platform())
    print("Machine:", platform.machine())

    if sys.version_info < (3, 12) or sys.version_info >= (3, 13):
        raise RuntimeError("Use Python 3.12.x for this project.")

    if platform.system() == "Windows" and platform.machine().lower() not in {"amd64", "x86_64"}:
        raise RuntimeError("This build target expects Windows x64.")


def check_imports() -> None:
    import PySide6.QtCore
    print("PySide6:", PySide6.QtCore.__version__)

    from piper import PiperVoice
    print("PiperVoice import: OK", PiperVoice)


def check_voices() -> None:
    expected = [
        "voices/en_US-lessac-high.onnx",
        "voices/en_US-lessac-high.onnx.json",
        "voices/de_DE-thorsten-high.onnx",
        "voices/de_DE-thorsten-high.onnx.json",
        "voices/tr_TR-fahrettin-medium.onnx",
        "voices/tr_TR-fahrettin-medium.onnx.json",
    ]

    missing = [item for item in expected if not Path(item).exists()]

    if missing:
        print("Missing voice files:")
        for item in missing:
            print(" -", item)
        raise RuntimeError("Download Piper voices before running the app.")

    print("Voice files: OK")


if __name__ == "__main__":
    check_python()
    check_imports()
    check_voices()
    print("Bootstrap check: OK")

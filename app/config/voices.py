from pathlib import Path
import sys

from app.utils.platform_utils import voices_dir


VOICE_PRESETS = {
    "English US - Lessac High": {
        "language_code": "en_US",
        "default_voice": "en_US-lessac-high",
        "model_file": "en_US-lessac-high.onnx",
    },
    "German - Thorsten High": {
        "language_code": "de_DE",
        "default_voice": "de_DE-thorsten-high",
        "model_file": "de_DE-thorsten-high.onnx",
    },
    "Turkish - Fahrettin Medium": {
        "language_code": "tr_TR",
        "default_voice": "tr_TR-fahrettin-medium",
        "model_file": "tr_TR-fahrettin-medium.onnx",
    },
    "Spanish Mexico - Claude High": {
        "language_code": "es_MX",
        "default_voice": "es_MX-claude-high",
        "model_file": "es_MX-claude-high.onnx",
    },
    "Spanish Spain - DaveFX Medium": {
        "language_code": "es_ES",
        "default_voice": "es_ES-davefx-medium",
        "model_file": "es_ES-davefx-medium.onnx",
    },
}


def get_voice_model_path(language: str) -> Path:
    if language not in VOICE_PRESETS:
        raise KeyError(f"Unknown language: {language}")
    name = VOICE_PRESETS[language]["model_file"]
    local = voices_dir() / name
    bundled = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2])) / "bundled_voices" / name
    for candidate in (local, bundled):
        if candidate.is_file() and Path(str(candidate) + ".json").is_file():
            return candidate
    return local


def get_default_voice_name(language: str) -> str:
    if language not in VOICE_PRESETS:
        raise KeyError(f"Unknown language: {language}")
    return VOICE_PRESETS[language]["default_voice"]

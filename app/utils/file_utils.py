from datetime import datetime
from pathlib import Path

from app.utils.platform_utils import audio_dir


def create_manual_output_file(language: str) -> Path:
    safe_language = language.lower().replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return audio_dir() / f"manual_{safe_language}_{timestamp}.wav"


def create_batch_output_file(input_txt_file: Path, output_dir: Path) -> Path:
    return output_dir / f"{input_txt_file.stem}.wav"

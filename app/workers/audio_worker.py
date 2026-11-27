from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot

from app.services.piper_tts_service import PiperTTSService
from app.utils.text_utils import clean_text, validate_text
from app.utils.file_utils import create_batch_output_file


class SingleAudioWorker(QObject):
    finished = Signal(str)
    error = Signal(str)
    progress = Signal(int)
    log = Signal(str)

    def __init__(self, text: str, voice_model: Path, output_file: Path):
        super().__init__()
        self.text = text
        self.voice_model = voice_model
        self.output_file = output_file
        self.tts_service = PiperTTSService()

    @Slot()
    def run(self) -> None:
        try:
            self.progress.emit(5)
            self.log.emit("Cleaning text...")

            text = clean_text(self.text)
            validate_text(text)

            self.progress.emit(20)
            self.log.emit("Generating WAV...")

            self.tts_service.generate_wav(text, self.voice_model, self.output_file)

            self.progress.emit(100)
            self.log.emit(f"Created: {self.output_file}")
            self.finished.emit(str(self.output_file))
        except Exception as exc:
            self.error.emit(str(exc))


class BatchAudioWorker(QObject):
    finished = Signal()
    error = Signal(str)
    progress = Signal(int)
    log = Signal(str)

    def __init__(self, input_dir: Path, output_dir: Path, voice_model: Path):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.voice_model = voice_model
        self.tts_service = PiperTTSService()

    @Slot()
    def run(self) -> None:
        try:
            txt_files = sorted(self.input_dir.glob("*.txt"))

            if not txt_files:
                raise FileNotFoundError(f"No .txt files found in: {self.input_dir}")

            self.output_dir.mkdir(parents=True, exist_ok=True)
            total = len(txt_files)
            self.log.emit(f"Found {total} TXT files.")

            for index, txt_file in enumerate(txt_files, start=1):
                try:
                    self.log.emit(f"Processing: {txt_file.name}")
                    raw_text = txt_file.read_text(encoding="utf-8")
                    text = clean_text(raw_text)
                    validate_text(text)

                    output_file = create_batch_output_file(txt_file, self.output_dir)
                    self.tts_service.generate_wav(text, self.voice_model, output_file)
                    self.log.emit(f"Created: {output_file}")
                except Exception as item_exc:
                    self.log.emit(f"Skipped/Error: {txt_file.name} -> {item_exc}")

                self.progress.emit(int(index / total * 100))

            self.log.emit("Batch completed.")
            self.finished.emit()
        except Exception as exc:
            self.error.emit(str(exc))

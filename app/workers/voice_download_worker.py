from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QObject, Signal, Slot

from app.config.voice_downloads import VoiceDownloadFile
from app.services.voice_download_service import download_voice_file


@dataclass(frozen=True)
class VoiceDownloadJob:
    label: str
    files: tuple[VoiceDownloadFile, ...]


class VoiceDownloadWorker(QObject):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal()
    error = Signal(str)

    def __init__(self, jobs: list[VoiceDownloadJob], overwrite: bool = True):
        super().__init__()
        self.jobs = jobs
        self.overwrite = overwrite

    @Slot()
    def run(self) -> None:
        try:
            all_files = [(job, file) for job in self.jobs for file in job.files]
            total_files = len(all_files)
            if total_files == 0:
                self.log.emit("No files selected")
                self.progress.emit(0)
                self.finished.emit()
                return

            for index, (job, file) in enumerate(all_files, start=1):
                base_progress = int((index - 1) * 100 / total_files)
                self.progress.emit(base_progress)
                self.log.emit(f"[{index}/{total_files}] {job.label}: {file.filename}")

                def file_progress(value: int) -> None:
                    total_progress = int(((index - 1) + value / 100) * 100 / total_files)
                    self.progress.emit(total_progress)

                download_voice_file(
                    file.url,
                    file.filename,
                    overwrite=self.overwrite,
                    progress_callback=file_progress,
                    log_callback=self.log.emit,
                )

            self.progress.emit(100)
            self.log.emit("Voice download completed")
            self.finished.emit()
        except Exception as exc:
            self.error.emit(str(exc))

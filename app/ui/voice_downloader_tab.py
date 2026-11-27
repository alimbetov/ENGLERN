from __future__ import annotations

from PySide6.QtCore import QThread, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QMessageBox,
    QCheckBox,
    QTextEdit,
    QGroupBox,
)

from app.config.voice_downloads import VOICE_DOWNLOAD_PRESETS
from app.utils.platform_utils import voices_dir
from app.workers.voice_download_worker import VoiceDownloadJob, VoiceDownloadWorker


class VoiceDownloaderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.thread: QThread | None = None
        self.worker: VoiceDownloadWorker | None = None
        self.checkboxes: list[tuple[QCheckBox, object]] = []

        layout = QVBoxLayout()

        title = QLabel("Download Piper voices into the voices folder")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)

        description = QLabel(
            "Select voices and click Download. Existing files will be overwritten. "
            "This can repair partial or corrupted ONNX files. "
            "If corporate SSL/proxy blocks Hugging Face, use scripts/download_voices_manual.ps1 or a browser."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        preset_box = QGroupBox("Voice presets")
        preset_layout = QVBoxLayout()

        for preset in VOICE_DOWNLOAD_PRESETS:
            checkbox = QCheckBox(f"{preset.label}  ({preset.voice_name})")
            checkbox.setChecked(True)
            self.checkboxes.append((checkbox, preset))
            preset_layout.addWidget(checkbox)

        preset_box.setLayout(preset_layout)
        layout.addWidget(preset_box)

        button_row = QHBoxLayout()
        self.download_button = QPushButton("Download selected")
        self.open_voices_button = QPushButton("Open voices folder")
        self.select_all_button = QPushButton("Select all")
        self.clear_button = QPushButton("Clear selection")

        self.download_button.clicked.connect(self.download_selected)
        self.open_voices_button.clicked.connect(self.open_voices_folder)
        self.select_all_button.clicked.connect(self.select_all)
        self.clear_button.clicked.connect(self.clear_selection)

        button_row.addWidget(self.download_button)
        button_row.addWidget(self.open_voices_button)
        button_row.addWidget(self.select_all_button)
        button_row.addWidget(self.clear_button)
        layout.addLayout(button_row)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Download log...")
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def select_all(self) -> None:
        for checkbox, _ in self.checkboxes:
            checkbox.setChecked(True)

    def clear_selection(self) -> None:
        for checkbox, _ in self.checkboxes:
            checkbox.setChecked(False)

    def selected_jobs(self) -> list[VoiceDownloadJob]:
        jobs: list[VoiceDownloadJob] = []
        for checkbox, preset in self.checkboxes:
            if checkbox.isChecked():
                jobs.append(
                    VoiceDownloadJob(
                        label=preset.label,
                        files=preset.files,
                    )
                )
        return jobs

    def download_selected(self) -> None:
        jobs = self.selected_jobs()
        if not jobs:
            QMessageBox.warning(self, "No selection", "Select at least one voice.")
            return

        self.download_button.setEnabled(False)
        self.progress.setValue(0)
        self.log_output.clear()
        self.append_log("Starting voice download...")
        self.append_log(f"Target folder: {voices_dir().resolve()}")

        self.thread = QThread()
        self.worker = VoiceDownloadWorker(jobs=jobs, overwrite=True)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.log.connect(self.append_log)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def append_log(self, message: str) -> None:
        self.log_output.append(message)

    def on_finished(self) -> None:
        self.download_button.setEnabled(True)
        QMessageBox.information(self, "Done", "Selected voices have been downloaded.")

    def on_error(self, message: str) -> None:
        self.download_button.setEnabled(True)
        self.append_log(f"ERROR: {message}")
        QMessageBox.critical(self, "Download error", message)

    def open_voices_folder(self) -> None:
        voices_dir().mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(voices_dir().resolve())))

from pathlib import Path

from PySide6.QtCore import QThread, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QProgressBar,
    QTextEdit,
    QFileDialog,
    QMessageBox,
)

from app.config.voices import VOICE_PRESETS, get_voice_model_path, get_default_voice_name
from app.utils.platform_utils import audio_dir
from app.workers.audio_worker import BatchAudioWorker


class FolderBatchTab(QWidget):
    def __init__(self):
        super().__init__()

        self.input_dir: Path | None = None
        self.output_dir: Path = audio_dir()
        self.thread: QThread | None = None
        self.worker: BatchAudioWorker | None = None

        layout = QVBoxLayout()

        self.language_combo = QComboBox()
        self.language_combo.addItems(list(VOICE_PRESETS.keys()))
        self.language_combo.currentTextChanged.connect(self.on_language_changed)

        self.voice_label = QLabel()
        self.on_language_changed(self.language_combo.currentText())

        language_row = QHBoxLayout()
        language_row.addWidget(QLabel("Language:"))
        language_row.addWidget(self.language_combo)
        language_row.addWidget(QLabel("Voice:"))
        language_row.addWidget(self.voice_label)

        self.input_label = QLabel("Input folder: not selected")
        self.output_label = QLabel(f"Output folder: {self.output_dir}")

        self.select_input_button = QPushButton("Select Input Folder")
        self.select_output_button = QPushButton("Select Output Folder")
        self.convert_button = QPushButton("Convert All TXT Files")
        self.open_output_button = QPushButton("Open Output Folder")

        self.select_input_button.clicked.connect(self.select_input_folder)
        self.select_output_button.clicked.connect(self.select_output_folder)
        self.convert_button.clicked.connect(self.convert_folder)
        self.open_output_button.clicked.connect(self.open_output_folder)

        input_row = QHBoxLayout()
        input_row.addWidget(self.select_input_button)
        input_row.addWidget(self.select_output_button)
        input_row.addWidget(self.convert_button)
        input_row.addWidget(self.open_output_button)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addLayout(language_row)
        layout.addWidget(self.input_label)
        layout.addWidget(self.output_label)
        layout.addLayout(input_row)
        layout.addWidget(self.progress)
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log)

        self.setLayout(layout)

    def on_language_changed(self, language: str) -> None:
        self.voice_label.setText(get_default_voice_name(language))

    def select_input_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select folder with TXT files")
        if folder:
            self.input_dir = Path(folder)
            self.input_label.setText(f"Input folder: {self.input_dir}")

    def select_output_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select output folder")
        if folder:
            self.output_dir = Path(folder)
            self.output_label.setText(f"Output folder: {self.output_dir}")

    def convert_folder(self) -> None:
        if not self.input_dir:
            QMessageBox.warning(self, "Input folder missing", "Select input folder first.")
            return

        language = self.language_combo.currentText()
        voice_model = get_voice_model_path(language)

        self.convert_button.setEnabled(False)
        self.progress.setValue(0)
        self.log.clear()

        self.thread = QThread()
        self.worker = BatchAudioWorker(self.input_dir, self.output_dir, voice_model)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.log.connect(self.append_log)
        self.worker.finished.connect(self.on_batch_finished)
        self.worker.error.connect(self.on_batch_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def append_log(self, message: str) -> None:
        self.log.append(message)

    def on_batch_finished(self) -> None:
        self.convert_button.setEnabled(True)
        self.progress.setValue(100)
        self.log.append("Done.")

    def on_batch_error(self, message: str) -> None:
        self.convert_button.setEnabled(True)
        QMessageBox.critical(self, "Batch error", message)
        self.log.append(f"ERROR: {message}")

    def open_output_folder(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.output_dir.resolve())))

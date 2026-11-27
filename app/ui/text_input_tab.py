from pathlib import Path

from PySide6.QtCore import QThread, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QComboBox,
    QPushButton,
    QProgressBar,
    QMessageBox,
)

from app.config.voices import VOICE_PRESETS, get_voice_model_path, get_default_voice_name
from app.utils.file_utils import create_manual_output_file
from app.utils.platform_utils import audio_dir
from app.workers.audio_worker import SingleAudioWorker
from app.ui.audio_player_widget import AudioPlayerWidget


class TextInputTab(QWidget):
    def __init__(self):
        super().__init__()

        self.thread: QThread | None = None
        self.worker: SingleAudioWorker | None = None
        self.last_audio_file: Path | None = None

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

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Type or paste text here...")

        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.status_label = QLabel("Status: ready")

        self.generate_button = QPushButton("Generate WAV")
        self.open_folder_button = QPushButton("Open Output Folder")
        self.audio_player = AudioPlayerWidget()

        self.generate_button.clicked.connect(self.generate_audio)
        self.open_folder_button.clicked.connect(self.open_output_folder)

        button_row = QHBoxLayout()
        button_row.addWidget(self.generate_button)
        button_row.addWidget(self.open_folder_button)

        layout.addLayout(language_row)
        layout.addWidget(QLabel("Text:"))
        layout.addWidget(self.text_input)
        layout.addLayout(button_row)
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        layout.addWidget(self.audio_player)

        self.setLayout(layout)

    def on_language_changed(self, language: str) -> None:
        self.voice_label.setText(get_default_voice_name(language))

    def generate_audio(self) -> None:
        text = self.text_input.toPlainText()
        language = self.language_combo.currentText()
        voice_model = get_voice_model_path(language)
        output_file = create_manual_output_file(language)

        self.generate_button.setEnabled(False)
        self.progress.setValue(0)
        self.status_label.setText("Status: starting...")

        self.thread = QThread()
        self.worker = SingleAudioWorker(text, voice_model, output_file)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.log.connect(self.status_label.setText)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_generation_finished(self, output_file: str) -> None:
        self.last_audio_file = Path(output_file)
        self.generate_button.setEnabled(True)
        self.audio_player.load_file(self.last_audio_file)
        self.status_label.setText(f"Status: created {output_file}")

    def on_generation_error(self, message: str) -> None:
        self.generate_button.setEnabled(True)
        self.status_label.setText("Status: error")
        QMessageBox.critical(self, "Generation error", message)

    def open_output_folder(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(audio_dir().resolve())))

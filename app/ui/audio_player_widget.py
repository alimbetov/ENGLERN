from pathlib import Path

from PySide6.QtCore import QUrl, Qt
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QComboBox,
)


class AudioPlayerWidget(QWidget):
    """Small WAV player with seek, volume and playback-speed controls."""

    def __init__(self):
        super().__init__()

        self.current_file: Path | None = None
        self.duration_ms = 0
        self.user_is_seeking = False

        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.audio_output.setVolume(0.8)
        self.player.setAudioOutput(self.audio_output)

        layout = QVBoxLayout()

        self.file_label = QLabel("Player: no audio loaded")
        self.time_label = QLabel("00:00 / 00:00")

        self.play_pause_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.play_pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)

        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.setEnabled(False)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setFixedWidth(130)

        self.speed_combo = QComboBox()
        self.speed_combo.addItem("0.50x", 0.50)
        self.speed_combo.addItem("0.75x", 0.75)
        self.speed_combo.addItem("1.00x", 1.00)
        self.speed_combo.addItem("1.25x", 1.25)
        self.speed_combo.addItem("1.50x", 1.50)
        self.speed_combo.addItem("1.75x", 1.75)
        self.speed_combo.addItem("2.00x", 2.00)
        self.speed_combo.setCurrentIndex(2)

        controls_row = QHBoxLayout()
        controls_row.addWidget(self.play_pause_button)
        controls_row.addWidget(self.stop_button)
        controls_row.addWidget(QLabel("Speed:"))
        controls_row.addWidget(self.speed_combo)
        controls_row.addWidget(QLabel("Volume:"))
        controls_row.addWidget(self.volume_slider)
        controls_row.addWidget(self.time_label)

        layout.addWidget(self.file_label)
        layout.addWidget(self.position_slider)
        layout.addLayout(controls_row)
        self.setLayout(layout)

        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.stop_button.clicked.connect(self.stop)
        self.speed_combo.currentIndexChanged.connect(self.change_speed)
        self.volume_slider.valueChanged.connect(self.change_volume)

        self.position_slider.sliderPressed.connect(self.on_slider_pressed)
        self.position_slider.sliderReleased.connect(self.on_slider_released)
        self.position_slider.sliderMoved.connect(self.on_slider_moved)

        self.player.positionChanged.connect(self.on_position_changed)
        self.player.durationChanged.connect(self.on_duration_changed)
        self.player.playbackStateChanged.connect(self.on_playback_state_changed)

    def load_file(self, file_path: Path) -> None:
        self.current_file = file_path
        self.player.setSource(QUrl.fromLocalFile(str(file_path.resolve())))
        self.player.setPlaybackRate(float(self.speed_combo.currentData()))

        self.file_label.setText(f"Player: {file_path.name}")
        self.play_pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.position_slider.setEnabled(True)
        self.play_pause_button.setText("Play")

    def toggle_play_pause(self) -> None:
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def stop(self) -> None:
        self.player.stop()
        self.position_slider.setValue(0)
        self.time_label.setText(f"00:00 / {self.format_ms(self.duration_ms)}")

    def change_speed(self) -> None:
        speed = float(self.speed_combo.currentData())
        self.player.setPlaybackRate(speed)

    def change_volume(self, value: int) -> None:
        self.audio_output.setVolume(value / 100.0)

    def on_slider_pressed(self) -> None:
        self.user_is_seeking = True

    def on_slider_released(self) -> None:
        self.user_is_seeking = False
        self.player.setPosition(self.position_slider.value())

    def on_slider_moved(self, value: int) -> None:
        self.time_label.setText(
            f"{self.format_ms(value)} / {self.format_ms(self.duration_ms)}"
        )

    def on_position_changed(self, position_ms: int) -> None:
        if not self.user_is_seeking:
            self.position_slider.setValue(position_ms)
        self.time_label.setText(
            f"{self.format_ms(position_ms)} / {self.format_ms(self.duration_ms)}"
        )

    def on_duration_changed(self, duration_ms: int) -> None:
        self.duration_ms = duration_ms
        self.position_slider.setRange(0, duration_ms)
        self.time_label.setText(f"00:00 / {self.format_ms(duration_ms)}")

    def on_playback_state_changed(self, state: QMediaPlayer.PlaybackState) -> None:
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_pause_button.setText("Pause")
        else:
            self.play_pause_button.setText("Play")

    @staticmethod
    def format_ms(value_ms: int) -> str:
        total_seconds = max(0, int(value_ms / 1000))
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

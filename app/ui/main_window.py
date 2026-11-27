from PySide6.QtWidgets import QMainWindow, QTabWidget

from app.ui.text_input_tab import TextInputTab
from app.ui.folder_batch_tab import FolderBatchTab
from app.ui.voice_downloader_tab import VoiceDownloaderTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ENGLERN")
        self.setMinimumSize(900, 650)

        tabs = QTabWidget()
        tabs.addTab(TextInputTab(), "Text Input")
        tabs.addTab(FolderBatchTab(), "Folder Batch")
        tabs.addTab(VoiceDownloaderTab(), "Voice Downloader")

        self.setCentralWidget(tabs)

import sys
from pathlib import Path
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow


def main() -> None:
    smoke = len(sys.argv) == 3 and sys.argv[1] == '--smoke-test'
    app = QApplication([sys.argv[0]] if smoke else sys.argv)
    app.setApplicationName('ENGLERN')
    window = MainWindow()
    window.show()
    if smoke:
        def complete():
            assert window.centralWidget().count() == 3
            Path(sys.argv[2]).write_text('ENGLERN GUI smoke PASS\n', encoding='utf-8')
            app.quit()
        QTimer.singleShot(1200, complete)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

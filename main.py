import sys
import os
from pathlib import Path
import logging
import faulthandler
from logging.handlers import RotatingFileHandler

def configure_startup_logging():
    from app.utils.platform_utils import app_root
    directory = app_root() / "logs"
    directory.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(directory / "startup.log", maxBytes=1024*1024, backupCount=2, encoding="utf-8")
    logging.basicConfig(level=logging.INFO, handlers=[handler], format="%(asctime)s %(levelname)s %(message)s", force=True)
    fault = (directory / "native-crash.log").open("a", encoding="utf-8")
    faulthandler.enable(file=fault, all_threads=True)
    logging.info("Starting ENGLERN platform=%s frozen=%s", sys.platform, getattr(sys, "frozen", False))
    return fault



def main() -> None:
    smoke = len(sys.argv) == 3 and sys.argv[1] in ('--smoke-test', '--standard-smoke-test', '--voice-smoke-test')
    from PySide6.QtCore import QTimer, qInstallMessageHandler
    from PySide6.QtWidgets import QApplication
    from app.ui.main_window import MainWindow
    qInstallMessageHandler(lambda kind, context, message: logging.info("Qt: %s", message))
    app = QApplication([sys.argv[0]] if smoke else sys.argv)
    app.setApplicationName('ENGLERN')
    window = MainWindow()
    window.show()
    logging.info("Main window shown")
    if sys.platform == "darwin" and not smoke:
        window.raise_()
        window.activateWindow()
        if os.environ.get("ENGLERN_NATIVE_LAUNCH_PROBE") == "1":
            def ready():
                if window.isVisible() and window.centralWidget().count() == 3:
                    from app.utils.platform_utils import app_root
                    (app_root() / "native-launch-ready").write_text("PASS\n", encoding="utf-8")
            QTimer.singleShot(1500, ready)
    if smoke:
        def complete():
            assert window.centralWidget().count() == 3
            if sys.argv[1] in ('--standard-smoke-test', '--voice-smoke-test'):
                assert os.environ.get("ENGLERN_SMOKE_ROOT"), "Isolated smoke profile required"
                from app.config.voices import get_voice_model_path
                model = get_voice_model_path("English US - LJ Speech High")
                if sys.argv[1] == '--standard-smoke-test':
                    root = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
                    assert not list((root / "bundled_voices").glob("*.onnx*"))
                    assert not model.exists()
            if sys.argv[1] == '--voice-smoke-test':
                import socket
                import tempfile
                import wave
                from app.config.voices import get_voice_model_path
                from app.services.piper_tts_service import PiperTTSService
                model = get_voice_model_path("English US - LJ Speech High")
                assert model.parent.name == "bundled_voices", "Bundled voice not selected"
                with tempfile.TemporaryDirectory() as directory:
                    output = Path(directory) / "probe.wav"
                    def deny_network(*args, **kwargs):
                        raise RuntimeError("Network disabled for Python synthesis probe")
                    from unittest.mock import patch
                    with patch.object(socket.socket, "connect", deny_network), patch.object(socket.socket, "connect_ex", deny_network), patch.object(socket, "create_connection", deny_network):
                        PiperTTSService().generate_wav("Welcome to ENGLERN.", model, output)
                    with wave.open(str(output), "rb") as wav:
                        assert wav.getframerate() == 22050
                        assert wav.getnchannels() == 1 and wav.getsampwidth() == 2
                        assert wav.getnframes() > 0 and any(wav.readframes(wav.getnframes()))
            Path(sys.argv[2]).write_text('ENGLERN GUI smoke PASS\n', encoding='utf-8')
            app.quit()
        QTimer.singleShot(1200, complete)
    sys.exit(app.exec())


if __name__ == '__main__':
    fault = None
    try:
        fault = configure_startup_logging()
        main()
    except Exception:
        logging.exception("Fatal startup failure")
        raise
    finally:
        if fault is not None:
            faulthandler.disable()
            fault.close()

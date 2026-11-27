from dataclasses import dataclass


@dataclass(frozen=True)
class VoiceDownloadFile:
    filename: str
    url: str


@dataclass(frozen=True)
class VoiceDownloadPreset:
    label: str
    language_code: str
    voice_name: str
    files: tuple[VoiceDownloadFile, ...]


VOICE_DOWNLOAD_PRESETS: tuple[VoiceDownloadPreset, ...] = (
    VoiceDownloadPreset(
        label="English US - LJ Speech High",
        language_code="en_US",
        voice_name="en_US-ljspeech-high",
        files=(
            VoiceDownloadFile(filename="en_US-ljspeech-high.onnx", url="https://huggingface.co/rhasspy/piper-voices/resolve/217ddc79818708b078d0d14a8fae9608b9d77141/en/en_US/ljspeech/high/en_US-ljspeech-high.onnx"),
            VoiceDownloadFile(filename="en_US-ljspeech-high.onnx.json", url="https://huggingface.co/rhasspy/piper-voices/resolve/217ddc79818708b078d0d14a8fae9608b9d77141/en/en_US/ljspeech/high/en_US-ljspeech-high.onnx.json"),
        ),
    ),
    VoiceDownloadPreset(
        label="English US - Lessac High",
        language_code="en_US",
        voice_name="en_US-lessac-high",
        files=(
            VoiceDownloadFile(
                filename="en_US-lessac-high.onnx",
                url="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx?download=true",
            ),
            VoiceDownloadFile(
                filename="en_US-lessac-high.onnx.json",
                url="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx.json?download=true",
            ),
        ),
    ),
    VoiceDownloadPreset(
        label="German - Thorsten High",
        language_code="de_DE",
        voice_name="de_DE-thorsten-high",
        files=(
            VoiceDownloadFile(
                filename="de_DE-thorsten-high.onnx",
                url="https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx?download=true",
            ),
            VoiceDownloadFile(
                filename="de_DE-thorsten-high.onnx.json",
                url="https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx.json?download=true",
            ),
        ),
    ),
    VoiceDownloadPreset(
        label="Turkish - Fahrettin Medium",
        language_code="tr_TR",
        voice_name="tr_TR-fahrettin-medium",
        files=(
            VoiceDownloadFile(
                filename="tr_TR-fahrettin-medium.onnx",
                url="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/tr/tr_TR/fahrettin/medium/tr_TR-fahrettin-medium.onnx",
            ),
            VoiceDownloadFile(
                filename="tr_TR-fahrettin-medium.onnx.json",
                url="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/tr/tr_TR/fahrettin/medium/tr_TR-fahrettin-medium.onnx.json",
            ),
        ),
    ),
    VoiceDownloadPreset(
        label="Spanish Mexico - Claude High",
        language_code="es_MX",
        voice_name="es_MX-claude-high",
        files=(
            VoiceDownloadFile(
                filename="es_MX-claude-high.onnx",
                url="https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/claude/high/es_MX-claude-high.onnx?download=true",
            ),
            VoiceDownloadFile(
                filename="es_MX-claude-high.onnx.json",
                url="https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/claude/high/es_MX-claude-high.onnx.json?download=true",
            ),
        ),
    ),
    VoiceDownloadPreset(
        label="Spanish Spain - DaveFX Medium",
        language_code="es_ES",
        voice_name="es_ES-davefx-medium",
        files=(
            VoiceDownloadFile(
                filename="es_ES-davefx-medium.onnx",
                url="https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx?download=true",
            ),
            VoiceDownloadFile(
                filename="es_ES-davefx-medium.onnx.json",
                url="https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json?download=true",
            ),
        ),
    ),
)

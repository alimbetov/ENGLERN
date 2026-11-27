from pathlib import Path
import wave

try:
    from piper import PiperVoice
except ImportError:  # compatibility with older package layout
    from piper.voice import PiperVoice  # type: ignore


class PiperTTSService:
    """In-process Piper TTS service.

    Important for PyInstaller: do not call `python -m piper` from a frozen app.
    Use the Python API so dependencies are bundled into the executable package.
    """

    _voice_cache: dict[str, PiperVoice] = {}

    def generate_wav(self, text: str, voice_model: Path, output_file: Path) -> Path:
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if not voice_model.exists():
            raise FileNotFoundError(f"Voice model not found: {voice_model}")

        config_file = Path(str(voice_model) + ".json")
        if not config_file.exists():
            raise FileNotFoundError(f"Voice config not found: {config_file}")

        voice = self._load_voice(voice_model, config_file)

        with wave.open(str(output_file), "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)

        return output_file

    @classmethod
    def _load_voice(cls, voice_model: Path, config_file: Path) -> PiperVoice:
        cache_key = str(voice_model.resolve())
        if cache_key not in cls._voice_cache:
            try:
                cls._voice_cache[cache_key] = PiperVoice.load(
                    str(voice_model),
                    str(config_file),
                )
            except TypeError:
                # Some Piper versions infer the JSON config from the ONNX path.
                cls._voice_cache[cache_key] = PiperVoice.load(str(voice_model))
        return cls._voice_cache[cache_key]

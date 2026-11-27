from __future__ import annotations

import os
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from app.utils.platform_utils import voices_dir

ProgressCallback = Callable[[int], None]
LogCallback = Callable[[str], None]


@dataclass(frozen=True)
class DownloadResult:
    output_path: Path
    bytes_written: int


class VoiceDownloadError(RuntimeError):
    pass


def _validate_downloaded_file(path: Path, filename: str | None = None) -> None:
    filename = filename or path.name
    if not path.exists():
        raise VoiceDownloadError(f"Downloaded file does not exist: {path}")

    size = path.stat().st_size
    if size <= 0:
        raise VoiceDownloadError(f"Downloaded file is empty: {path.name}")

    with path.open("rb") as stream:
        header = stream.read(512).lower()
    if header.startswith(b"<!doctype html") or header.startswith(b"<html"):
        raise VoiceDownloadError(
            f"Downloaded file looks like an HTML page, not a model/config: {path.name}"
        )

    if b"git-lfs.github.com/spec" in header:
        raise VoiceDownloadError(
            f"Downloaded file is a Git LFS pointer, not the real model file: {path.name}"
        )

    if filename.endswith(".onnx") and size < 1_000_000:
        raise VoiceDownloadError(
            f"ONNX model is suspiciously small ({size} bytes): {path.name}"
        )

    if filename.endswith(".onnx.json") and size < 100:
        raise VoiceDownloadError(
            f"ONNX config JSON is suspiciously small ({size} bytes): {path.name}"
        )


def download_voice_file(
    url: str,
    filename: str,
    *,
    overwrite: bool = True,
    progress_callback: ProgressCallback | None = None,
    log_callback: LogCallback | None = None,
) -> DownloadResult:
    target_dir = voices_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    output_path = target_dir / filename

    if output_path.exists() and not overwrite:
        if log_callback:
            log_callback(f"Skip existing file: {output_path.name}")
        _validate_downloaded_file(output_path)
        return DownloadResult(output_path=output_path, bytes_written=output_path.stat().st_size)

    if log_callback:
        log_callback(f"Downloading: {filename}")

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AcademicAudioStudio/0.1 PiperVoiceDownloader"},
    )

    fd, temp_name = tempfile.mkstemp(prefix=f".{filename}.", suffix=".download", dir=target_dir)
    os.close(fd)
    temp_path = Path(temp_name)

    bytes_written = 0
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            status = getattr(response, "status", None)
            if status and status >= 400:
                raise VoiceDownloadError(f"HTTP error {status} for {url}")

            expected_length_raw = response.headers.get("Content-Length")
            expected_length = int(expected_length_raw) if expected_length_raw else None

            with temp_path.open("wb") as output:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    output.write(chunk)
                    bytes_written += len(chunk)

                    if expected_length and progress_callback:
                        progress_callback(min(100, int(bytes_written * 100 / expected_length)))

            if expected_length is not None and bytes_written != expected_length:
                raise VoiceDownloadError(
                    f"Incomplete download for {filename}: got {bytes_written}, expected {expected_length} bytes"
                )

        _validate_downloaded_file(temp_path, filename)
        temp_path.replace(output_path)

        if progress_callback:
            progress_callback(100)
        if log_callback:
            mb = bytes_written / 1024 / 1024
            log_callback(f"Saved: {output_path.name} ({mb:.1f} MB)")

        return DownloadResult(output_path=output_path, bytes_written=bytes_written)

    except Exception:
        try:
            temp_path.unlink(missing_ok=True)
        finally:
            raise

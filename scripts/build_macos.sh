#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync --locked --group build --no-build
uv run --locked --no-sync python -m PyInstaller --noconfirm --clean --windowed --onedir --name ENGLERN --collect-all piper --collect-all onnxruntime main.py

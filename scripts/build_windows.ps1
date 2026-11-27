$ErrorActionPreference = 'Stop'
Set-Location "$PSScriptRoot\.."
uv sync --locked --group build --no-build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
uv run --locked --no-sync python -m PyInstaller --noconfirm --clean --windowed --onedir --name ENGLERN --collect-all piper --collect-all onnxruntime main.py
exit $LASTEXITCODE

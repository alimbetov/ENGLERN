$ErrorActionPreference = 'Stop'
Set-Location "$PSScriptRoot\.."
uv run --locked --no-sync python main.py
exit $LASTEXITCODE

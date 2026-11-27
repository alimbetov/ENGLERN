$ErrorActionPreference = 'Stop'
Set-Location "$PSScriptRoot\.."
uv python install 3.12.16
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
uv sync --locked --group dev --group test --group build --no-build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
New-Item -ItemType Directory -Force -Path voices,audio,texts | Out-Null

$ErrorActionPreference = "Stop"

Set-Location "$PSScriptRoot\.."
. .\.venv\Scripts\Activate.ps1
python bootstrap_check.py

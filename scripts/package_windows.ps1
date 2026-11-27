param([string]$Iscc = "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe", [string]$VoiceDir = $env:ENGLERN_VOICE_DIR)
$ErrorActionPreference = 'Stop'
Set-Location "$PSScriptRoot\.."
if (-not (Test-Path $Iscc)) { throw 'Install Inno Setup 6 or specify -Iscc.' }
if ((Get-FileHash uv.lock -Algorithm SHA256).Hash.ToLower() -ne 'c68e7e8cb941f0f21892f27f2b7ab03e619b0f19763cbe8478eb4195643e3c98') { throw 'Lock digest mismatch' }
function Check { if ($LASTEXITCODE -ne 0) { throw "Native command failed: $LASTEXITCODE" } }
uv python install 3.12.16; Check
uv lock --check; Check
uv sync --locked --group build --no-build; Check
uv run --locked --no-sync python -c "import platform,sys; assert sys.version_info[:3]==(3,12,16) and sys.platform=='win32' and platform.machine().lower()=='amd64'"; Check
$voiceArgs = @()
if ($VoiceDir) {
    $VoiceDir = (Resolve-Path $VoiceDir).Path
    uv run --locked --no-sync python scripts/verify_bundled_voice.py $VoiceDir; Check
    foreach ($name in @('en_US-lessac-high.onnx','en_US-lessac-high.onnx.json')) {
        $voiceArgs += @('--add-data', ((Join-Path $VoiceDir $name) + ':bundled_voices'))
    }
}
uv run --locked --no-sync python -m PyInstaller @voiceArgs --noconfirm --clean --windowed --onedir --name ENGLERN --collect-all piper --collect-all onnxruntime main.py; Check
function Smoke([string]$Exe) {
    $marker = Join-Path $env:TEMP ("englern-" + [guid]::NewGuid() + '.txt')
    $mode = if ($VoiceDir) { '--voice-smoke-test' } else { '--smoke-test' }
    $p = Start-Process -FilePath $Exe -ArgumentList @($mode, ('"' + $marker + '"')) -PassThru
    if (-not $p.WaitForExit(180000)) { $p.Kill(); throw 'GUI smoke timeout' }
    if ($p.ExitCode -ne 0 -or -not (Test-Path $marker)) { throw 'GUI smoke failed' }
    if ((Get-Content $marker -Raw).Trim() -ne 'ENGLERN GUI smoke PASS') { throw 'Invalid smoke marker' }
    Remove-Item $marker
}
Smoke (Resolve-Path 'dist/ENGLERN/ENGLERN.exe').Path
& $Iscc 'packaging/windows.iss'; Check
$installer = (Resolve-Path 'release/ENGLERN-0.1.0-alpha.1-win-x64-setup.exe').Path
if ($env:CI -eq 'true') {
    $target = Join-Path $env:RUNNER_TEMP ('englern-install-' + [guid]::NewGuid())
    $p = Start-Process $installer -ArgumentList @('/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/SP-',('/DIR="'+$target+'"')) -Wait -PassThru
    if ($p.ExitCode -ne 0) { throw 'Installation failed' }
    Smoke (Join-Path $target 'ENGLERN.exe')
    $p = Start-Process (Join-Path $target 'unins000.exe') -ArgumentList '/VERYSILENT','/NORESTART' -Wait -PassThru
    if ($p.ExitCode -ne 0 -or (Test-Path (Join-Path $target 'ENGLERN.exe'))) { throw 'Uninstall failed' }
}
(Get-FileHash $installer -Algorithm SHA256).Hash.ToLower() | Set-Content "$installer.sha256" -Encoding ascii

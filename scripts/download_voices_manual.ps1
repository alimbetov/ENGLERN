$ErrorActionPreference = "Stop"

Set-Location "$PSScriptRoot\.."

New-Item -ItemType Directory -Force -Path voices | Out-Null

$voices = @(
    @{
        Name = "English US - Lessac High"
        Files = @(
            @{ Url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx?download=true"; Out = "voices\en_US-lessac-high.onnx" },
            @{ Url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx.json?download=true"; Out = "voices\en_US-lessac-high.onnx.json" }
        )
    },
    @{
        Name = "German - Thorsten High"
        Files = @(
            @{ Url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx?download=true"; Out = "voices\de_DE-thorsten-high.onnx" },
            @{ Url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx.json?download=true"; Out = "voices\de_DE-thorsten-high.onnx.json" }
        )
    },
    @{
        Name = "Turkish - Fahrettin Medium"
        Files = @(
            @{ Url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/tr/tr_TR/fahrettin/medium/tr_TR-fahrettin-medium.onnx"; Out = "voices\tr_TR-fahrettin-medium.onnx" },
            @{ Url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/tr/tr_TR/fahrettin/medium/tr_TR-fahrettin-medium.onnx.json"; Out = "voices\tr_TR-fahrettin-medium.onnx.json" }
        )
    },
    @{
        Name = "Spanish Mexico - Claude High"
        Files = @(
            @{ Url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/claude/high/es_MX-claude-high.onnx?download=true"; Out = "voices\es_MX-claude-high.onnx" },
            @{ Url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/claude/high/es_MX-claude-high.onnx.json?download=true"; Out = "voices\es_MX-claude-high.onnx.json" }
        )
    },
    @{
        Name = "Spanish Spain - DaveFX Medium"
        Files = @(
            @{ Url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx?download=true"; Out = "voices\es_ES-davefx-medium.onnx" },
            @{ Url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json?download=true"; Out = "voices\es_ES-davefx-medium.onnx.json" }
        )
    }
)

foreach ($voice in $voices) {
    Write-Host "Downloading $($voice.Name)..."
    foreach ($file in $voice.Files) {
        Write-Host " -> $($file.Out)"
        curl.exe -L $file.Url -o $file.Out

        if (!(Test-Path $file.Out)) {
            throw "File was not created: $($file.Out)"
        }

        $size = (Get-Item $file.Out).Length
        if ($size -lt 100) {
            throw "Downloaded file is suspiciously small: $($file.Out) ($size bytes)"
        }
    }
}

Write-Host "Voice download completed. Files in .\voices:"
Get-ChildItem .\voices\*.onnx* | Select-Object Name, Length

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
edition="${ENGLERN_EDITION:-standard}"
version=0.1.0-alpha.2
case "$edition" in
    standard) [[ -z "${ENGLERN_VOICE_DIR:-}" ]] || { echo "Standard must not bundle voices" >&2; exit 1; } ;;
    offline) [[ -n "${ENGLERN_VOICE_DIR:-}" ]] || { echo "Offline requires verified voice directory" >&2; exit 1; } ;;
    *) echo "Invalid edition" >&2; exit 1 ;;
esac
[[ $(uname -s) == Darwin && $(uname -m) == arm64 ]]
[[ $(shasum -a 256 uv.lock | cut -d' ' -f1) == c68e7e8cb941f0f21892f27f2b7ab03e619b0f19763cbe8478eb4195643e3c98 ]]
uv python install 3.12.16
uv lock --check
uv sync --locked --group build --no-build
uv run --locked --no-sync python -c 'import sys,platform; assert sys.version_info[:3]==(3,12,16) and platform.machine()=="arm64"'
voice_args=()
mode=--standard-smoke-test
if [[ -n "${ENGLERN_VOICE_DIR:-}" ]]; then
    uv run --locked --no-sync python scripts/verify_bundled_voice.py "$ENGLERN_VOICE_DIR"
    for name in en_US-ljspeech-high.onnx en_US-ljspeech-high.onnx.json MODEL_CARD VOICE-EVIDENCE.json VOICE-NOTICE.txt; do
        voice_args+=(--add-data "$ENGLERN_VOICE_DIR/$name:bundled_voices")
    done
    mode=--voice-smoke-test
fi
uv run --locked --no-sync python -m PyInstaller ${voice_args[@]+"${voice_args[@]}"} --noconfirm --clean --windowed --onedir --name ENGLERN --osx-bundle-identifier com.englern.desktop --collect-all piper --collect-all onnxruntime main.py
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
smoke() {
    local marker="$stage/smoke.txt" pid
    rm -f "$marker"
    rm -rf "$stage/profile"
    ENGLERN_SMOKE_ROOT="$stage/profile" QT_QPA_PLATFORM=offscreen "$1" "$mode" "$marker" & pid=$!
    for ((i=0;i<180;i++)); do
        if ! kill -0 "$pid" 2>/dev/null; then wait "$pid"; grep -Fxq 'ENGLERN GUI smoke PASS' "$marker"; return; fi
        sleep 1
    done
    kill "$pid" 2>/dev/null || true
    wait "$pid" || true
    return 1
}
smoke "$PWD/dist/ENGLERN.app/Contents/MacOS/ENGLERN"
mkdir -p release "$stage/image"
ditto dist/ENGLERN.app "$stage/image/ENGLERN.app"
ln -s /Applications "$stage/image/Applications"
image="$PWD/release/ENGLERN-$version-macos-arm64-$edition.dmg"
hdiutil create -ov -format UDZO -volname ENGLERN -srcfolder "$stage/image" "$image"
hdiutil verify "$image"
mkdir "$stage/mount"
hdiutil attach -readonly -nobrowse -mountpoint "$stage/mount" "$image"
trap 'hdiutil detach "$stage/mount" || true; rm -rf "$stage"' EXIT
ditto "$stage/mount/ENGLERN.app" "$stage/installed.app"
smoke "$stage/installed.app/Contents/MacOS/ENGLERN"
hdiutil detach "$stage/mount"
trap 'rm -rf "$stage"' EXIT
shasum -a 256 "$image" > "$image.sha256"

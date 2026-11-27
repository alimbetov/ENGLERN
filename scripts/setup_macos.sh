#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv python install 3.12.16
uv sync --locked --group dev --group test --group build --no-build
mkdir -p voices audio texts
